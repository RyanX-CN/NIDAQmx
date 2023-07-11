from QPSLClass.Base import *
from QPSLClass.QPSLGroupBox import QPSLGroupBox
from QPSLClass.QPSLLabel import QPSLLabel
from QPSLClass.QPSLLayout import QPSLHBoxLayout
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLLineEdit(QLineEdit, QPSLWidgetBase):

    def __init__(self, parent: QWidget, object_name: str):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)


class QPSLTextLineEdit(QPSLGroupBox):
    sig_return_pressed = pyqtSignal([], [str])
    sig_editing_finished = pyqtSignal([], [str])

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 key_text: str = "key",
                 stretch: Tuple[int, int] = (1, 2)):
        super().__init__(parent=parent, object_name=object_name, title="")
        self.setupUi()
        self.setupLogic()
        self.set_key(key_text=key_text)
        self.set_stretch(sizes=stretch)

    def setupUi(self):
        self.setLayout(QPSLHBoxLayout(self))
        self.layout.add_widget(widget=QPSLLabel(self, object_name="label_key"))
        self.layout.add_widget(
            widget=QPSLLineEdit(self, object_name="edit_text"))

    def setupLogic(self):
        connect_direct(self.edit_text.returnPressed, self.on_return_pressed)
        connect_direct(self.edit_text.editingFinished,
                       self.on_editing_finished)
        connect_direct(self.sig_return_pressed, self.sig_editing_finished)
        connect_direct(self.sig_return_pressed[str],
                       self.sig_editing_finished[str])

    @property
    def layout(self) -> QPSLHBoxLayout:
        return super().layout()

    @property
    def label_key(self) -> QPSLLabel:
        return self.layout.get_widget(0)

    @property
    def edit_text(self) -> QPSLLineEdit:
        return self.layout.get_widget(1)

    def set_key(self, key_text: str):
        self.label_key.setText(key_text)

    def set_stretch(self, sizes: Tuple[int, int]):
        self.layout.set_stretch(sizes)

    def text(self):
        return self.edit_text.text()

    def clear(self):
        self.edit_text.clear()

    def set_text(self, text: str):
        self.edit_text.setText(text)

    def set_read_only(self, b: bool):
        self.edit_text.setReadOnly(b)

    def on_return_pressed(self):
        self.sig_return_pressed.emit()
        self.sig_return_pressed[str].emit(self.text())

    def on_editing_finished(self):
        self.sig_editing_finished.emit()
        self.sig_editing_finished[str].emit(self.text())

    def set_echo_mode(self, echo_mode: QLineEdit.EchoMode):
        self.edit_text.setEchoMode(echo_mode)
