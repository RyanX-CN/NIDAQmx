from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLProgressDialog(QProgressDialog, QPSLWidgetBase):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 title: str,
                 min: int,
                 max: int,
                 width: int = 800,
                 height: int = 20):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.setWindowTitle(title)
        self.setRange(min, max)
        self.resize(width, height)