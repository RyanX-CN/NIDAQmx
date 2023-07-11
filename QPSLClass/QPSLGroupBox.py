from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLGroupBox(QGroupBox, QPSLWidgetBase):

    def __init__(self, parent: QWidget, object_name: str, title: str = ""):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        if title:
            self.setTitle(title)
