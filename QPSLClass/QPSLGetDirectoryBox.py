from QPSLClass.Base import *
from QPSLClass.QPSLGroupList import QPSLHorizontalGroupList
from QPSLClass.QPSLLabel import QPSLLabel, QPSLScalePixmapLabel
from QPSLClass.QPSLPushButton import QPSLPushButton


class QPSLGetDirectoryBox(QPSLHorizontalGroupList):
    sig_path_changed = pyqtSignal(str)

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 text="Dir:",
                 path: Optional[str] = None,
                 stretch: Tuple[int, int, int] = (3, 6, 1)):
        super().__init__(parent=parent, object_name=object_name, title="")
        self.m_path = None
        self.add_widget(widget=QPSLLabel(self,
                                         object_name="label_key",
                                         text=text,
                                         frame_shape=QFrame.Shape.NoFrame))
        self.add_widget(widget=QPSLPushButton(
            self, object_name="btn_select", text="select"))
        self.add_widget(widget=QPSLScalePixmapLabel(
            self, object_name="label_icon", frame_shape=QFrame.Shape.NoFrame))
        self.set_path(path=path)
        self.set_stretch(sizes=stretch)
        self.set_icon_checked(checked=False)
        connect_direct(self.btn_select.sig_clicked, self.on_select_clicked)

    def on_select_clicked(self):
        res = QFileDialog.getExistingDirectory(None, directory=self.m_path)
        self.set_path(path=res)

    def set_path(self, path: str):
        if path:
            self.m_path = path
            self.btn_select.set_tooltip_enable()
            self.btn_select.setToolTip(path)
            self.set_icon_checked(checked=True)
            self.sig_path_changed.emit(path)
        else:
            self.btn_select.set_tooltip_disable()
            self.set_icon_checked(checked=False)

    def get_path(self):
        return self.m_path

    def set_icon_checked(self, checked: bool):
        if checked:
            self.label_icon.set_pixmap(QPixmap("resources/checked.png"))
        else:
            self.label_icon.set_pixmap(QPixmap("resources/unchecked.png"))

    @property
    def label(self) -> QPSLLabel:
        return self.get_widget(0)

    @property
    def btn_select(self) -> QPSLPushButton:
        return self.get_widget(1)

    @property
    def label_icon(self) -> QPSLScalePixmapLabel:
        return self.get_widget(2)