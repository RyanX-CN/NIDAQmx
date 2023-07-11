from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLRadioButton(QRadioButton, QPSLWidgetBase):
    sig_getChecked = pyqtSignal([], [QRadioButton], [str])

    def __init__(self, parent: QWidget, object_name: str, text: str = "press"):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.setText(text)
        connect_direct(self.clicked, self.on_clicked)

    def on_clicked(self):
        self.sig_getChecked.emit()
        self.sig_getChecked[QRadioButton].emit(self)
        self.sig_getChecked[str].emit(self.text())