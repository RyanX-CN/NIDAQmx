from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLMessageBox(QMessageBox, QPSLWidgetBase):

    def __init__(self, parent: QWidget, object_name: str, window_title: str,
                 text: str):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.setWindowTitle(window_title)
        self.setText(text)