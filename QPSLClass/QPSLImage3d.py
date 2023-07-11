from QPSLClass.Base import *
from QPSLClass.QPSLPushButton import QPSLPushButton, QPSLToggleButton
from QPSLClass.QPSLGetOpenFileBox import QPSLGetOpenFileBox
from QPSLClass.QPSLObjectBase import QPSLObjectBase
from QPSLClass.QPSLGroupList import QPSLVerticalGroupList, QPSLHorizontalGroupList, QPSLGridGroupList
from QPSLClass.QPSLSpinBox import QPSLSpinBox, QPSLDoubleSpinBox
from QPSLClass.QPSLSlider import QPSLSlider
from QPSLClass.QPSLTrackedLabel import QPSLTrackedScalePixmapLabel
from QPSLClass.QPSLListWidget import QPSLTextListWidget
from QPSLClass.QPSLWaiting import QPSLWaitingDialog


class QPSLImage3d(QPSLVerticalGroupList):
    sig_worker_delete = pyqtSignal()
    sig_mouse_click = pyqtSignal(QPoint)

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 window_title: str = ""):
        super(QPSLImage3d, self).__init__(parent=parent,
                                          object_name=object_name)
        self.m_bit_width = 16
        self.m_max_color = 65535
        self.m_byte_width = 2
        self.m_image_format = QImage.Format.Format_Grayscale16
        self.m_image: np.ndarray = None
        self.m_mutex = QMutex()
        self.m_tasks = deque()
        self.setWindowTitle(window_title)
        self.setupUi()
        self.setupStyle()
        self.setupLogic()
        self.resize(200, 200)

    @QPSLObjectBase.log_decorator()
    def setupUi(self):
        self.add_widget(widget=QPSLTrackedScalePixmapLabel(
            self, object_name="label_image"))

        self.add_widget(widget=QPSLHorizontalGroupList(
            self, object_name="box_slider_control"))
        self.box_slider_control.add_widget(
            widget=QPSLSlider(self.box_slider_control,
                              object_name="slider",
                              orientation=Qt.Orientation.Horizontal,
                              min=0,
                              max=1,
                              value=0))
        self.slider.set_tooltip_enable()
        self.box_slider_control.add_widget(
            widget=QPSLPushButton(self.box_slider_control,
                                  object_name="btn_change_axis",
                                  text="axis x"))
        self.box_slider_control.set_stretch(sizes=(8, 1))

        self.add_widget(
            widget=QPSLHorizontalGroupList(self, object_name="box_settings"))
        self.box_settings.add_widget(widget=QPSLSpinBox(self.box_settings,
                                                        object_name="spin_low",
                                                        min=0,
                                                        max=self.m_max_color,
                                                        value=0,
                                                        prefix="low: "))
        self.box_settings.add_widget(
            widget=QPSLSpinBox(self.box_settings,
                               object_name="spin_high",
                               min=0,
                               max=self.m_max_color,
                               value=self.m_max_color,
                               prefix="high: "))
        self.box_settings.add_widget(
            widget=QPSLSpinBox(self.box_settings,
                               object_name="spin_ratio",
                               min=0,
                               max=self.m_max_color,
                               value=5,
                               prefix="gray ratio: "))
        self.set_stretch(sizes=(20, 2, 1))

    @QPSLObjectBase.log_decorator()
    def setupStyle(self):
        return

    @QPSLObjectBase.log_decorator()
    def setupLogic(self):
        connect_direct(self.btn_change_axis.sig_clicked, self.change_axis)
        connect_direct(self.slider.valueChanged, self.show_image_at)
        connect_direct(self.spin_low.sig_editing_finished,
                       self.show_current_image)
        connect_direct(self.spin_high.sig_editing_finished,
                       self.show_current_image)
        connect_direct(self.spin_gray_ratio.sig_editing_finished,
                       self.show_current_image)
        connect_direct(self.label_image.sig_mouse_click,
                       self.show_click_position)

    @QPSLObjectBase.log_decorator()
    def set_image_data(self, image_data: np.ndarray):
        self.m_image = image_data
        self.set_axis_x(i=0)

    @QPSLObjectBase.log_decorator()
    def set_axis_x(self, i: int):
        self.btn_change_axis.set_text(text='axis x')
        if self.m_image is not None:
            self.slider.setRange(0, self.m_image.shape[2] - 1)
        else:
            self.slider.setRange(0, 1)
        self.show_image_at(i)

    @QPSLObjectBase.log_decorator()
    def set_axis_y(self, i: int):
        self.btn_change_axis.set_text(text='axis y')
        if self.m_image is not None:
            self.slider.setRange(0, self.m_image.shape[1] - 1)
        else:
            self.slider.setRange(0, 1)
        self.show_image_at(i)

    @QPSLObjectBase.log_decorator()
    def set_axis_z(self, i: int):
        self.btn_change_axis.set_text(text='axis z')
        if self.m_image is not None:
            self.slider.setRange(0, self.m_image.shape[0] - 1)
        else:
            self.slider.setRange(0, 1)
        self.show_image_at(i)

    @QPSLObjectBase.log_decorator()
    def change_axis(self):
        if self.btn_change_axis.text() == "axis x":
            self.set_axis_y(i=0)
        elif self.btn_change_axis.text() == "axis y":
            self.set_axis_z(i=0)
        else:
            self.set_axis_x(i=0)

    @QPSLObjectBase.log_decorator()
    def show_current_image(self):
        if self.m_image is None:
            return
        i = int(self.slider.value())
        gray_low = self.spin_low.value()
        gray_high = self.spin_high.value()
        gray_ratio = self.spin_gray_ratio.value()
        self.m_tasks.append(
            (self.btn_change_axis.text()[-1], i, self.m_image, gray_low,
             gray_high, gray_ratio, self.m_byte_width, self.m_max_color,
             int(self.m_image_format)))
        self.slider.setToolTip("{0}".format(i))

        def handle_image():
            self.m_mutex.lock()
            axis: str
            i: int
            image: np.ndarray
            gray_low: int
            gray_high: int
            gray_ratio: float
            byte_width: int
            max_color: int
            image_format: QImage.Format
            if self.m_tasks:
                while self.m_tasks:
                    axis, i, image, gray_low, gray_high, gray_ratio, byte_width, max_color, image_format = self.m_tasks.popleft(
                    )
                img: np.ndarray
                if axis == 'x':
                    img = image[:, :, i].copy()
                elif axis == 'y':
                    img = image[:, i, :].copy()
                else:
                    img = image[i, :, :].copy()
                need_mask = np.logical_and(img >= gray_low, img <= gray_high)
                not_need_mask = np.logical_or(img < gray_low, img > gray_high)
                img[not_need_mask] = 0
                Min, Max = np.min(img[need_mask]), np.max(img[need_mask])
                if Min != Max:
                    r = gray_ratio
                    if r: img *= int(r)
                    else: img *= max_color // Max
                qimg = QImage(img.data.tobytes(), img.shape[1], img.shape[0],
                              img.shape[1] * byte_width, image_format)
                self.label_image.set_pixmap(pixmap=QPixmap.fromImage(qimg))
            self.m_mutex.unlock()

        QThreadPool.globalInstance().start(handle_image)

    @QPSLObjectBase.log_decorator()
    def show_image_at(self, i: int):
        if self.m_image is None:
            return
        self.slider.setValue(i)
        self.show_current_image()

    @QPSLObjectBase.log_decorator()
    def show_click_position(self, pos: QPointF):
        if self.m_image is None:
            return
        shape: Tuple[int, int]
        if self.btn_change_axis.text() == "axis x":
            shape = self.m_image.shape[:2]
        elif self.btn_change_axis.text() == "axis y":
            shape = self.m_image.shape[0], self.m_image.shape[2]
        else:
            shape = self.m_image.shape[1:]
        self.sig_mouse_click.emit(
            QPoint(int(shape[1] * pos.x()), int(shape[0] * pos.y())))

    @property
    def label_image(self) -> QPSLTrackedScalePixmapLabel:
        return self.get_widget(0)

    @property
    def box_slider_control(self) -> QPSLHorizontalGroupList:
        return self.get_widget(1)

    @property
    def box_settings(self) -> QPSLHorizontalGroupList:
        return self.get_widget(2)

    @property
    def slider(self) -> QPSLSlider:
        return self.box_slider_control.get_widget(0)

    @property
    def btn_change_axis(self) -> QPSLPushButton:
        return self.box_slider_control.get_widget(1)

    @property
    def spin_low(self) -> QPSLSpinBox:
        return self.box_settings.get_widget(0)

    @property
    def spin_high(self) -> QPSLSpinBox:
        return self.box_settings.get_widget(1)

    @property
    def spin_gray_ratio(self) -> QPSLSpinBox:
        return self.box_settings.get_widget(2)


class QPSLImage3dCompare(QPSLVerticalGroupList):
    sig_worker_delete = pyqtSignal()
    sig_mouse_click = pyqtSignal(QPoint)

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 window_title: str = ""):
        super(QPSLImage3dCompare, self).__init__(parent=parent,
                                                 object_name=object_name)
        self.m_bit_width = 16
        self.m_max_color = 65535
        self.m_byte_width = 2
        self.m_image_format = QImage.Format.Format_Grayscale16
        self.m_image1: np.ndarray = None
        self.m_image2: np.ndarray = None
        self.m_mutex = QMutex()
        self.m_tasks = deque()
        self.setWindowTitle(window_title)
        self.setupUi()
        self.setupStyle()
        self.setupLogic()

    @QPSLObjectBase.log_decorator()
    def setupUi(self):
        self.add_widget(
            widget=QPSLHorizontalGroupList(self, object_name="box_images"))
        self.box_images.add_widget(widget=QPSLTrackedScalePixmapLabel(
            self.box_images, object_name="label_image1"))
        self.box_images.add_widget(widget=QPSLTrackedScalePixmapLabel(
            self.box_images, object_name="label_image2"))

        self.add_widget(widget=QPSLHorizontalGroupList(
            self, object_name="box_slider_control"))
        self.box_slider_control.add_widget(
            widget=QPSLSlider(self.box_slider_control,
                              object_name="slider",
                              orientation=Qt.Orientation.Horizontal,
                              min=0,
                              max=1,
                              value=0))
        self.slider.set_tooltip_enable()
        self.box_slider_control.add_widget(
            widget=QPSLPushButton(self.box_slider_control,
                                  object_name="btn_change_axis",
                                  text="axis x"))
        self.box_slider_control.set_stretch(sizes=(8, 1))

        self.add_widget(
            widget=QPSLHorizontalGroupList(self, object_name="box_settings"))
        self.box_settings.add_widget(widget=QPSLSpinBox(self.box_settings,
                                                        object_name="spin_low",
                                                        min=0,
                                                        max=self.m_max_color,
                                                        value=0,
                                                        prefix="low: "))
        self.box_settings.add_widget(
            widget=QPSLSpinBox(self.box_settings,
                               object_name="spin_high",
                               min=0,
                               max=self.m_max_color,
                               value=self.m_max_color,
                               prefix="high: "))
        self.box_settings.add_widget(
            widget=QPSLSpinBox(self.box_settings,
                               object_name="spin_ratio",
                               min=0,
                               max=self.m_max_color,
                               value=5,
                               prefix="gray ratio: "))
        self.set_stretch(sizes=(20, 2, 1))

    @QPSLObjectBase.log_decorator()
    def setupStyle(self):
        return

    @QPSLObjectBase.log_decorator()
    def setupLogic(self):
        connect_direct(self.btn_change_axis.sig_clicked, self.change_axis)
        connect_direct(self.slider.valueChanged, self.show_image_at)
        connect_direct(self.spin_low.sig_editing_finished,
                       self.show_current_image)
        connect_direct(self.spin_high.sig_editing_finished,
                       self.show_current_image)
        connect_direct(self.spin_gray_ratio.sig_editing_finished,
                       self.show_current_image)

    @QPSLObjectBase.log_decorator()
    def set_image_data(self, image_data1: np.ndarray, image_data2: np.ndarray):
        self.m_image1 = image_data1
        self.m_image2 = image_data2
        self.set_axis_x(i=0)

    @QPSLObjectBase.log_decorator()
    def set_axis_x(self, i: int):
        self.btn_change_axis.set_text(text='axis x')
        if self.m_image1 is not None:
            self.slider.setRange(0, self.m_image1.shape[2] - 1)
        else:
            self.slider.setRange(0, 1)
        self.show_image_at(i)

    @QPSLObjectBase.log_decorator()
    def set_axis_y(self, i: int):
        self.btn_change_axis.set_text(text='axis y')
        if self.m_image1 is not None:
            self.slider.setRange(0, self.m_image1.shape[1] - 1)
        else:
            self.slider.setRange(0, 1)
        self.show_image_at(i)

    @QPSLObjectBase.log_decorator()
    def set_axis_z(self, i: int):
        self.btn_change_axis.set_text(text='axis z')
        if self.m_image1 is not None:
            self.slider.setRange(0, self.m_image1.shape[0] - 1)
        else:
            self.slider.setRange(0, 1)
        self.show_image_at(i)

    @QPSLObjectBase.log_decorator()
    def change_axis(self):
        if self.btn_change_axis.text() == "axis x":
            self.set_axis_y(i=0)
        elif self.btn_change_axis.text() == "axis y":
            self.set_axis_z(i=0)
        else:
            self.set_axis_x(i=0)

    @QPSLObjectBase.log_decorator()
    def show_current_image(self):
        if self.m_image1 is None:
            return
        i = int(self.slider.value())
        gray_low = self.spin_low.value()
        gray_high = self.spin_high.value()
        gray_ratio = self.spin_gray_ratio.value()
        self.m_tasks.append(
            (self.btn_change_axis.text()[-1], i, self.m_image1, self.m_image2,
             gray_low, gray_high, gray_ratio, self.m_byte_width,
             self.m_max_color, int(self.m_image_format)))
        self.slider.setToolTip("{0}".format(i))

        def handle_image():
            self.m_mutex.lock()
            axis: str
            i: int
            image1: np.ndarray
            image2: np.ndarray
            gray_low: int
            gray_high: int
            gray_ratio: float
            byte_width: int
            max_color: int
            image_format: QImage.Format
            if self.m_tasks:
                while self.m_tasks:
                    axis, i, image1, image2, gray_low, gray_high, gray_ratio, byte_width, max_color, image_format = self.m_tasks.popleft(
                    )
                img1: np.ndarray
                img2: np.ndarray
                if axis == 'x':
                    img1 = image1[:, :, i].copy()
                    img2 = image2[:, :, i].copy()
                elif axis == 'y':
                    img1 = image1[:, i, :].copy()
                    img2 = image2[:, i, :].copy()
                else:
                    img1 = image1[i, :, :].copy()
                    img2 = image2[i, :, :].copy()
                need_mask1 = np.logical_and(img1 >= gray_low,
                                            img1 <= gray_high)
                need_mask2 = np.logical_and(img2 >= gray_low,
                                            img2 <= gray_high)
                not_need_mask = np.logical_or(img1 < gray_low,
                                              img1 > gray_high)
                not_need_mask = np.logical_or(img2 < gray_low,
                                              img2 > gray_high)
                img1[not_need_mask] = 0
                img2[not_need_mask] = 0
                Min1, Max1 = np.min(img1[need_mask1]), np.max(img1[need_mask1])
                if Min1 != Max1:
                    r = gray_ratio
                    if r: img1 *= int(r)
                    else: img1 *= max_color // Max1
                Min2, Max2 = np.min(img2[need_mask2]), np.max(img2[need_mask2])
                if Min2 != Max2:
                    r = gray_ratio
                    if r: img2 *= int(r)
                    else: img2 *= max_color // Max2
                qimg1 = QImage(img1.data.tobytes(), img1.shape[1],
                               img1.shape[0], img1.shape[1] * byte_width,
                               image_format)
                qimg2 = QImage(img2.data.tobytes(), img2.shape[1],
                               img2.shape[0], img2.shape[1] * byte_width,
                               image_format)
                self.label_image1.set_pixmap(pixmap=QPixmap.fromImage(qimg1))
                self.label_image2.set_pixmap(pixmap=QPixmap.fromImage(qimg2))
            self.m_mutex.unlock()

        QThreadPool.globalInstance().start(handle_image)

    @QPSLObjectBase.log_decorator()
    def show_image_at(self, i: int):
        if self.m_image1 is None:
            return
        self.slider.setValue(i)
        self.show_current_image()

    @QPSLObjectBase.log_decorator()
    def show_click_position(self, pos: QPointF):
        if self.m_image1 is None:
            return
        shape: Tuple[int, int]
        if self.btn_change_axis.text() == "axis x":
            shape = self.m_image1.shape[:2]
        elif self.btn_change_axis.text() == "axis y":
            shape = self.m_image1.shape[0], self.m_image1.shape[2]
        else:
            shape = self.m_image1.shape[1:]
        self.sig_mouse_click.emit(
            QPoint(int(shape[1] * pos.x()), int(shape[0] * pos.y())))

    @property
    def box_images(self) -> QPSLHorizontalGroupList:
        return self.get_widget(0)

    @property
    def label_image1(self) -> QPSLTrackedScalePixmapLabel:
        return self.box_images.get_widget(0)

    @property
    def label_image2(self) -> QPSLTrackedScalePixmapLabel:
        return self.box_images.get_widget(1)

    @property
    def box_slider_control(self) -> QPSLHorizontalGroupList:
        return self.get_widget(1)

    @property
    def box_settings(self) -> QPSLHorizontalGroupList:
        return self.get_widget(2)

    @property
    def slider(self) -> QPSLSlider:
        return self.box_slider_control.get_widget(0)

    @property
    def btn_change_axis(self) -> QPSLPushButton:
        return self.box_slider_control.get_widget(1)

    @property
    def spin_low(self) -> QPSLSpinBox:
        return self.box_settings.get_widget(0)

    @property
    def spin_high(self) -> QPSLSpinBox:
        return self.box_settings.get_widget(1)

    @property
    def spin_gray_ratio(self) -> QPSLSpinBox:
        return self.box_settings.get_widget(2)


class QPSLImage3dDivision(QPSLVerticalGroupList):
    sig_worker_delete = pyqtSignal()
    sig_mouse_click = pyqtSignal(QPoint)
    sig_to_divide = pyqtSignal(deque)
    sig_to_divide_all = pyqtSignal(list)

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 window_title: str = ""):
        super(QPSLImage3dDivision, self).__init__(parent=parent,
                                                  object_name=object_name)
        self.m_bit_width = 16
        self.m_max_color = 65535
        self.m_byte_width = 2
        self.m_image_format = QImage.Format.Format_Grayscale16
        self.m_image: np.ndarray = None
        self.m_mutex1 = QMutex()
        self.m_mutex2 = QMutex()
        self.m_tasks1 = deque()
        self.m_tasks3 = deque()
        self.m_tasks2 = deque()
        self.setWindowTitle(window_title)
        self.setupUi()
        self.setupStyle()
        self.setupLogic()
        self.resize(700, 500)

    @QPSLObjectBase.log_decorator()
    def setupUi(self):
        self.add_widget(
            widget=QPSLHorizontalGroupList(self, object_name="box_images"))
        self.box_images.add_widget(widget=QPSLTrackedScalePixmapLabel(
            self.box_images, object_name="label_image1"))
        self.box_images.add_widget(widget=QPSLTrackedScalePixmapLabel(
            self.box_images, object_name="label_image2"))

        self.add_widget(widget=QPSLHorizontalGroupList(
            self, object_name="box_slider_control"))
        self.box_slider_control.add_widget(
            widget=QPSLSlider(self.box_slider_control,
                              object_name="slider",
                              orientation=Qt.Orientation.Horizontal,
                              min=0,
                              max=1,
                              value=0))
        self.slider.set_tooltip_enable()
        self.box_slider_control.add_widget(
            widget=QPSLPushButton(self.box_slider_control,
                                  object_name="btn_change_axis",
                                  text="axis x"))
        self.box_slider_control.set_stretch(sizes=(8, 1))

        self.add_widget(
            widget=QPSLHorizontalGroupList(self, object_name="box_settings"))
        self.box_settings.add_widget(widget=QPSLSpinBox(self.box_settings,
                                                        object_name="spin_low",
                                                        min=0,
                                                        max=self.m_max_color,
                                                        value=0,
                                                        prefix="low: "))
        self.box_settings.add_widget(
            widget=QPSLSpinBox(self.box_settings,
                               object_name="spin_high",
                               min=0,
                               max=self.m_max_color,
                               value=self.m_max_color,
                               prefix="high: "))
        self.box_settings.add_widget(
            widget=QPSLSpinBox(self.box_settings,
                               object_name="spin_ratio",
                               min=0,
                               max=self.m_max_color,
                               value=5,
                               prefix="gray ratio: "))

        self.add_widget(
            widget=QPSLHorizontalGroupList(self, object_name="box_parameters"))
        self.box_parameters.add_widget(
            widget=QPSLSpinBox(self.box_parameters,
                               object_name="spin_divide_down_ration",
                               min=0,
                               max=10000,
                               value=40,
                               prefix="divide down ratio: "))
        self.box_parameters.add_widget(
            widget=QPSLSpinBox(self.box_parameters,
                               object_name="spin_ninary_thresh",
                               min=0,
                               max=65535,
                               value=320,
                               prefix="binary thresh: "))
        self.box_parameters.add_widget(
            widget=QPSLDoubleSpinBox(self.box_parameters,
                                     object_name="spin_radius",
                                     min=0,
                                     max=10000,
                                     value=5,
                                     prefix="radius: ",
                                     decimals=3))
        self.box_parameters.add_widget(widget=QPSLPushButton(
            self.box_parameters, object_name="btn_save", text="save"))

        self.add_widget(widget=QPSLTextListWidget(
            self, object_name="list_memory", capacity=0))

        self.add_widget(widget=QPSLPushButton(
            self, object_name="btn_divide_all", text="divide_all"))

        self.add_widget(widget=QPSLGetOpenFileBox(
            self,
            object_name="box_save_path",
            text="save into:",
        ))

        self.set_stretch(sizes=(20, 2, 1, 1, 2, 2, 2))

    @QPSLObjectBase.log_decorator()
    def setupStyle(self):
        return

    @QPSLObjectBase.log_decorator()
    def setupLogic(self):
        connect_direct(self.btn_change_axis.sig_clicked, self.change_axis)
        connect_direct(self.slider.valueChanged, self.show_image_at)
        connect_direct(self.spin_low.sig_editing_finished,
                       self.show_current_image)
        connect_direct(self.spin_high.sig_editing_finished,
                       self.show_current_image)
        connect_direct(self.spin_gray_ratio.sig_editing_finished,
                       self.show_current_image)

        connect_direct(self.btn_change_axis.sig_clicked, self.call_divide)
        connect_direct(self.slider.valueChanged, self.on_slider_move)
        connect_direct(self.spin_divide_down_ratio.sig_editing_finished,
                       self.call_divide)
        connect_direct(self.spin_binary_thresh.sig_editing_finished,
                       self.call_divide)
        connect_direct(self.spin_gray_ratio.sig_editing_finished,
                       self.call_divide)
        connect_direct(self.btn_save.sig_clicked, self.save_frame)

        connect_direct(self.list_memory.doubleClicked,
                       self.list_memory.remove_selected_item)

        connect_direct(self.btn_divide_all.sig_clicked, self.start_divide_all)

    @QPSLObjectBase.log_decorator()
    def set_image_data(self, image_data: np.ndarray):
        self.m_image = image_data
        self.set_axis_x(i=0)

    @QPSLObjectBase.log_decorator()
    def set_axis_x(self, i: int):
        self.btn_change_axis.set_text(text='axis x')
        if self.m_image is not None:
            self.slider.setRange(0, self.m_image.shape[2] - 1)
        else:
            self.slider.setRange(0, 1)
        self.show_image_at(i)

    @QPSLObjectBase.log_decorator()
    def set_axis_y(self, i: int):
        self.btn_change_axis.set_text(text='axis y')
        if self.m_image is not None:
            self.slider.setRange(0, self.m_image.shape[1] - 1)
        else:
            self.slider.setRange(0, 1)
        self.show_image_at(i)

    @QPSLObjectBase.log_decorator()
    def set_axis_z(self, i: int):
        self.btn_change_axis.set_text(text='axis z')
        if self.m_image is not None:
            self.slider.setRange(0, self.m_image.shape[0] - 1)
        else:
            self.slider.setRange(0, 1)
        self.show_image_at(i)

    @QPSLObjectBase.log_decorator()
    def change_axis(self):
        if self.btn_change_axis.text() == "axis x":
            self.set_axis_y(i=0)
        elif self.btn_change_axis.text() == "axis y":
            self.set_axis_z(i=0)
        else:
            self.set_axis_x(i=0)

    @QPSLObjectBase.log_decorator()
    def show_current_image(self):
        if self.m_image is None:
            return
        i = int(self.slider.value())
        gray_low = self.spin_low.value()
        gray_high = self.spin_high.value()
        gray_ratio = self.spin_gray_ratio.value()
        self.m_tasks1.append(
            (self.btn_change_axis.text()[-1], i, self.m_image, gray_low,
             gray_high, gray_ratio, self.m_byte_width, self.m_max_color,
             int(self.m_image_format)))
        self.slider.setToolTip("{0}".format(i))

        def handle_image():
            self.m_mutex1.lock()
            axis: str
            i: int
            image: np.ndarray
            gray_low: int
            gray_high: int
            gray_ratio: float
            byte_width: int
            max_color: int
            image_format: QImage.Format
            if self.m_tasks1:
                while self.m_tasks1:
                    axis, i, image, gray_low, gray_high, gray_ratio, byte_width, max_color, image_format = self.m_tasks1.popleft(
                    )
                img: np.ndarray
                if axis == 'x':
                    img = image[:, :, i].copy()
                elif axis == 'y':
                    img = image[:, i, :].copy()
                else:
                    img = image[i, :, :].copy()
                need_mask = np.logical_and(img >= gray_low, img <= gray_high)
                not_need_mask = np.logical_or(img < gray_low, img > gray_high)
                img[not_need_mask] = 0
                Min, Max = np.min(img[need_mask]), np.max(img[need_mask])
                if Min != Max:
                    r = gray_ratio
                    if r: img *= int(r)
                    else: img *= max_color // Max
                qimg = QImage(img.data.tobytes(), img.shape[1], img.shape[0],
                              img.shape[1] * byte_width, image_format)
                self.label_image1.set_pixmap(pixmap=QPixmap.fromImage(qimg))
            self.m_mutex1.unlock()

        QThreadPool.globalInstance().start(handle_image)

    @QPSLObjectBase.log_decorator()
    def show_image_at(self, i: int):
        if self.m_image is None:
            return
        self.slider.setValue(i)
        self.show_current_image()

    @QPSLObjectBase.log_decorator()
    def show_click_position(self, pos: QPointF):
        if self.m_image is None:
            return
        shape: Tuple[int, int]
        if self.btn_change_axis.text() == "axis x":
            shape = self.m_image.shape[:2]
        elif self.btn_change_axis.text() == "axis y":
            shape = self.m_image.shape[0], self.m_image.shape[2]
        else:
            shape = self.m_image.shape[1:]
        self.sig_mouse_click.emit(
            QPoint(int(shape[1] * pos.x()), int(shape[0] * pos.y())))

    @QPSLObjectBase.log_decorator()
    def on_slider_move(self, index: int):
        self.call_divide()

    @QPSLObjectBase.log_decorator()
    def call_divide(self):
        if self.m_image is None:
            return
        image = self.m_image
        i = self.slider.value()
        axis = self.btn_change_axis.text()[-1]
        if axis == 'x':
            img = image[:, :, i]
        elif axis == 'y':
            img = image[:, i, :]
        else:
            img = image[i, :, :]
        divide_down_ratio = self.spin_divide_down_ratio.value()
        binary_thresh = self.spin_binary_thresh.value()
        radius = self.spin_radius.value()
        self.m_tasks3.append((img, divide_down_ratio, binary_thresh, radius))
        self.sig_to_divide.emit(self.m_tasks3)

    @QPSLObjectBase.log_decorator()
    def get_divide_result(self, img: np.ndarray):
        gray_low = self.spin_low.value()
        gray_high = self.spin_high.value()
        gray_ratio = self.spin_gray_ratio.value()
        self.m_tasks2.append(
            (img, gray_low, gray_high, gray_ratio, self.m_byte_width,
             self.m_max_color, int(self.m_image_format)))

        def handle_image():
            self.m_mutex2.lock()
            img: np.ndarray
            gray_low: int
            gray_high: int
            gray_ratio: float
            byte_width: int
            max_color: int
            image_format: QImage.Format
            if self.m_tasks2:
                while self.m_tasks2:
                    img, gray_low, gray_high, gray_ratio, byte_width, max_color, image_format = self.m_tasks2.popleft(
                    )
                need_mask = np.logical_and(img >= gray_low, img <= gray_high)
                not_need_mask = np.logical_or(img < gray_low, img > gray_high)
                img[not_need_mask] = 0
                Min, Max = np.min(img[need_mask]), np.max(img[need_mask])
                if Min != Max:
                    r = gray_ratio
                    if r: img *= int(r)
                    else: img *= max_color // Max
                qimg = QImage(img.data.tobytes(), img.shape[1], img.shape[0],
                              img.shape[1] * byte_width, image_format)
                self.label_image2.set_pixmap(pixmap=QPixmap.fromImage(qimg))
            self.m_mutex2.unlock()

        QThreadPool.globalInstance().start(handle_image)

    @QPSLObjectBase.log_decorator()
    def save_frame(self):
        index = self.slider.value()
        divide_down_ratio = self.spin_divide_down_ratio.value()
        binary_thresh = self.spin_binary_thresh.value()
        radius = self.spin_radius.value()
        bigger_index = 0
        while bigger_index < self.list_memory.count() and int(
                self.list_memory.item(bigger_index).text().split(',')
            [0]) < index:
            bigger_index += 1
        if bigger_index < self.list_memory.count() and int(
                self.list_memory.item(bigger_index).text().split(',')
            [0]) == index:
            self.list_memory.remove_row(row=bigger_index)
        self.list_memory.insert_item(row=bigger_index,
                                     text="{0},{1},{2},{3}".format(
                                         index, divide_down_ratio,
                                         binary_thresh, radius))

    @QPSLObjectBase.log_decorator()
    def start_divide_all(self):
        if self.m_image is None:
            return
        mem = []
        for i in range(self.list_memory.count()):
            mem.append(self.list_memory.item(i).text().split(','))
        cursor = 0
        image = self.m_image
        axis = self.btn_change_axis.text()[-1]
        tasks = []
        while True:
            if cursor == len(mem):
                break
            start = int(mem[cursor][0])
            divide_down_ratio = int(mem[cursor][1])
            binary_thresh = int(mem[cursor][2])
            radius = float(mem[cursor][3])
            if cursor == len(mem) - 1:
                if axis == 'x':
                    end = image.shape[2] - 1
                elif axis == 'y':
                    end = image.shape[1] - 1
                else:
                    end = image.shape[0] - 1
            else:
                end = int(mem[cursor + 1][0]) - 1
            for i in range(start, end + 1):
                if axis == 'x':
                    img = image[:, :, i]
                elif axis == 'y':
                    img = image[:, i, :]
                else:
                    img = image[i, :, :]
                tasks.append((img, divide_down_ratio, binary_thresh, radius))
            cursor += 1

        self.sig_to_divide_all.emit(tasks)

        self.m_waiting = QPSLWaitingDialog(None,
                                           object_name="waiting",
                                           size=QSize(200, 200))
        self.m_waiting.move(
            self.mapToGlobal(self.rect().center()) - QPoint(100, 100))
        self.m_waiting.exec()

    @QPSLObjectBase.log_decorator()
    def on_divide_all_over(self, res: np.ndarray):
        self.m_waiting.accept()
        self.m_waiting.deleteLater()
        del self.m_waiting
        tifffile.imwrite(self.box_save_into.get_path(), res)

    @property
    def box_images(self) -> QPSLHorizontalGroupList:
        return self.get_widget(0)

    @property
    def label_image1(self) -> QPSLTrackedScalePixmapLabel:
        return self.box_images.get_widget(0)

    @property
    def label_image2(self) -> QPSLTrackedScalePixmapLabel:
        return self.box_images.get_widget(1)

    @property
    def box_slider_control(self) -> QPSLHorizontalGroupList:
        return self.get_widget(1)

    @property
    def box_settings(self) -> QPSLHorizontalGroupList:
        return self.get_widget(2)

    @property
    def box_parameters(self) -> QPSLHorizontalGroupList:
        return self.get_widget(3)

    @property
    def list_memory(self) -> QPSLTextListWidget:
        return self.get_widget(4)

    @property
    def btn_divide_all(self) -> QPSLPushButton:
        return self.get_widget(5)

    @property
    def box_save_into(self) -> QPSLGetOpenFileBox:
        return self.get_widget(6)

    @property
    def slider(self) -> QPSLSlider:
        return self.box_slider_control.get_widget(0)

    @property
    def btn_change_axis(self) -> QPSLPushButton:
        return self.box_slider_control.get_widget(1)

    @property
    def spin_low(self) -> QPSLSpinBox:
        return self.box_settings.get_widget(0)

    @property
    def spin_high(self) -> QPSLSpinBox:
        return self.box_settings.get_widget(1)

    @property
    def spin_gray_ratio(self) -> QPSLSpinBox:
        return self.box_settings.get_widget(2)

    @property
    def spin_divide_down_ratio(self) -> QPSLSpinBox:
        return self.box_parameters.get_widget(0)

    @property
    def spin_binary_thresh(self) -> QPSLSpinBox:
        return self.box_parameters.get_widget(1)

    @property
    def spin_radius(self) -> QPSLDoubleSpinBox:
        return self.box_parameters.get_widget(2)

    @property
    def btn_save(self) -> QPSLPushButton:
        return self.box_parameters.get_widget(3)
