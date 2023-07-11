from QPSLClass.Base import *
from QPSLClass.QPSLLayout import QPSLHBoxLayout, QPSLVBoxLayout, QPSLBoxLayout
from QPSLClass.QPSLLabel import QPSLLabel
from QPSLClass.QPSLGroupList import QPSLLinearGroupList
from QPSLClass.QPSLSpinBox import QPSLSpinBox, QPSLDoubleSpinBox
from QPSLClass.QPSLSplitter import QPSLSplitter
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLSlider(QSlider, QPSLWidgetBase):
    sig_ratio_mouse_novered = pyqtSignal(tuple)
    sig_ratio_clicked = pyqtSignal(tuple)
    sig_enter = pyqtSignal()
    sig_leave = pyqtSignal()

    def __init__(self, parent: QWidget, object_name: str,
                 orientation: Qt.Orientation, min: int, max: int, value: int):
        super().__init__(parent=parent, orientation=orientation)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.m_dragable = True
        self.setRange(min, max)
        self.setValue(value)
        self.setMinimumSize(14, 14)
        self.setMouseTracking(True)

    def set_dragable(self, b: bool):
        self.m_dragable = b

    def convert_position_to_ratio(self, pos: QPointF):
        if self.orientation() == Qt.Orientation.Horizontal:
            f = (pos.x() - 6) / (self.width() - 13)
        else:
            f = 1 - (pos.y() - 6) / (self.height() - 13)
        return (1 - f, f)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.sig_ratio_clicked.emit(
                self.convert_position_to_ratio(pos=event.pos()))
        if self.m_dragable:
            return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.sig_ratio_mouse_novered.emit(
            self.convert_position_to_ratio(pos=event.pos()))
        return super().mouseMoveEvent(event)

    def enterEvent(self, event: QMouseEvent):
        if self.isEnabled():
            self.sig_enter.emit()
        return super().enterEvent(event)

    def leaveEvent(self, event: QMouseEvent):
        if self.isEnabled():
            self.sig_leave.emit()
        return super().leaveEvent(event)


class QPSLFloatSlider(QPSLSlider):
    sig_value_clicked = pyqtSignal(float)
    sig_value_mouse_novered = pyqtSignal(float)
    sig_value_changed = pyqtSignal(float)

    def __init__(self, parent: QWidget, object_name: str,
                 orientation: Qt.Orientation, min: float, max: float,
                 value: float, decimals: int):
        self.m_minimum = min
        self.m_maximum = max
        self.m_value = value
        super().__init__(parent=parent,
                         object_name=object_name,
                         orientation=orientation,
                         min=0,
                         max=10**decimals,
                         value=int(10**decimals * ((value - min) /
                                                   (max - min))))
        self.set_dragable(b=False)
        connect_direct(self.sig_ratio_clicked, self.on_ratio_clicked)
        connect_direct(self.sig_ratio_mouse_novered,
                       self.on_ratio_mouse_novered)

    def set_decimals(self, decimals: int):
        super().setRange(0, 10**decimals)
        self.update_slider()

    def set_range(self, min: int, max: int) -> None:
        self.m_minimum = min
        self.m_maximum = max
        self.update_slider()

    def set_value(self, val: float):
        if val < self.m_minimum or val > self.m_maximum:
            return
        self.m_value = val
        self.update_slider()

    def get_value(self):
        return self.m_value

    def update_slider(self):
        self.setValue(self.map_to_internal_value(value=self.m_value))
        self.sig_value_changed.emit(self.m_value)

    def ratio_to_value(self, ratio: Tuple[float, float]):
        return ratio[0] * self.m_minimum + ratio[1] * self.m_maximum

    def map_to_internal_value(self, value: float):
        return int(self.maximum() * ((value - self.m_minimum) /
                                     (self.m_maximum - self.m_minimum)))

    def on_ratio_clicked(self, ratio):
        val = self.ratio_to_value(ratio=ratio)
        if self.minimum() <= self.map_to_internal_value(
                value=val) <= self.maximum():
            self.sig_value_clicked.emit(val)

    def on_ratio_mouse_novered(self, ratio):
        val = self.ratio_to_value(ratio=ratio)
        if self.minimum() <= self.map_to_internal_value(
                value=val) <= self.maximum():
            self.sig_value_mouse_novered.emit(val)


class QPSLComboSlider(QPSLLinearGroupList):
    sig_value_changed = pyqtSignal(float)
    sig_clicked = pyqtSignal(float)
    sig_enter = pyqtSignal()
    sig_leave = pyqtSignal()

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 orientation: Qt.Orientation,
                 title="",
                 value=0,
                 min=0,
                 max=20,
                 decimals=4):
        super().__init__(parent=parent,
                         object_name=object_name,
                         orientation=orientation,
                         title=title)
        self.m_orientation = orientation
        self.m_decimals = decimals
        self.m_tooltip = QPSLLabel(None, object_name="tooltip")
        self.m_tooltip.setWindowFlags(Qt.WindowType.CustomizeWindowHint
                                      | Qt.WindowType.FramelessWindowHint)
        self.m_tooltip.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground)
        self.set_tooltip_invisible()
        self.setupUi()
        self.setupLogic()
        self.set_decimals(decimals=decimals)
        self.set_range(min=min, max=max)
        self.set_value(value=value)

    def setupUi(self):

        def setup_slider_show():
            self.add_widget(
                widget=QPSLLinearGroupList(self,
                                           object_name="slider_show",
                                           orientation=self.m_orientation))
            p1, p2 = QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
            if self.m_orientation == Qt.Orientation.Vertical:
                p1, p2 = p2, p1
            self.slider_show.setSizePolicy(p1, p2)
            self.slider_show.add_widget(
                widget=QPSLFloatSlider(self.slider_show,
                                       object_name="slider",
                                       orientation=self.m_orientation,
                                       value=100,
                                       min=-500,
                                       max=1000,
                                       decimals=self.m_decimals))
            self.slider_show.add_widget(
                widget=QPSLDoubleSpinBox(self.slider_show,
                                         object_name="spin_value",
                                         value=0,
                                         decimals=min(3, self.m_decimals)))
            self.slider.setSizePolicy(self.slider_show.sizePolicy())
            self.slider.setMinimumWidth(50)
            self.spin_value.set_read_only(b=True)

        def setup_augument():
            self.add_widget(
                widget=QPSLLinearGroupList(self,
                                           object_name="augument_show",
                                           orientation=self.m_orientation))
            self.augument_show.add_widget(
                widget=QPSLDoubleSpinBox(self.augument_show,
                                         object_name="spin_min",
                                         prefix="min: ",
                                         decimals=min(3, self.m_decimals)))
            self.spin_min.set_read_only(b=True)
            self.augument_show.add_widget(
                widget=QPSLDoubleSpinBox(self.augument_show,
                                         object_name="spin_max",
                                         prefix="max: ",
                                         decimals=min(3, self.m_decimals)))
            self.spin_max.set_read_only(b=True)
            self.augument_show.add_widget(
                widget=QPSLSpinBox(self.augument_show,
                                   object_name="spin_decimals",
                                   min=0,
                                   max=9,
                                   value=self.m_decimals,
                                   prefix="decimals: "))
            self.spin_min.setMinimumWidth(90)
            self.spin_min.setMaximumWidth(160)
            self.spin_max.setMinimumWidth(90)
            self.spin_max.setMaximumWidth(160)
            self.spin_decimals.setMinimumWidth(130)

        setup_slider_show()
        setup_augument()

    def setupLogic(self):
        connect_direct(self.slider.sig_value_changed, self.sig_value_changed)
        connect_direct(self.sig_value_changed, self.spin_value.setValue)
        connect_direct(self.spin_decimals.sig_editing_finished[int],
                       self.set_decimals)
        connect_direct(self.slider.sig_value_clicked, self.sig_clicked)
        connect_direct(self.slider.sig_value_mouse_novered, self.set_tooltip)
        connect_direct(self.slider.sig_enter, self.sig_enter)
        connect_direct(self.slider.sig_leave, self.sig_leave)
        connect_direct(self.sig_enter, self.set_tooltip_visible)
        connect_direct(self.sig_leave, self.set_tooltip_invisible)

    @property
    def slider_show(self) -> QPSLLinearGroupList:
        return self.layout.get_widget(0)

    @property
    def slider(self) -> QPSLFloatSlider:
        return self.slider_show.get_widget(0)

    @property
    def spin_value(self) -> QPSLDoubleSpinBox:
        return self.slider_show.get_widget(1)

    @property
    def augument_show(self) -> QPSLLinearGroupList:
        return self.layout.get_widget(1)

    @property
    def spin_min(self) -> QPSLDoubleSpinBox:
        return self.augument_show.get_widget(0)

    @property
    def spin_max(self) -> QPSLDoubleSpinBox:
        return self.augument_show.get_widget(1)

    @property
    def spin_decimals(self) -> QPSLSpinBox:
        return self.augument_show.get_widget(2)

    def set_tooltip_visible(self):
        self.m_tooltip.setVisible(True)

    def set_tooltip_invisible(self):
        self.m_tooltip.setVisible(False)

    def value(self):
        return self.slider.get_value()

    def set_value(self, value: float):
        self.slider.set_value(val=value)

    def range(self):
        return self.spin_min.value(), self.spin_max.value()

    def set_range(self, min: float, max: float):
        self.slider.set_range(min=min, max=max)
        self.spin_min.setValue(min)
        self.spin_max.setValue(max)

    def set_decimals(self, decimals: int):
        self.m_decimals = decimals
        self.slider.set_decimals(decimals)
        self.spin_value.setDecimals(decimals)
        self.spin_min.setDecimals(decimals)
        self.spin_max.setDecimals(decimals)
        self.spin_decimals.setValue(decimals)

    def set_tooltip(self, value: float):
        self.m_tooltip.setText("%.1f" % value)
        self.m_tooltip.adjustSize()
        self.m_tooltip.move(QCursor.pos() - QPoint(0, 40))
        self.m_tooltip.raise_()
