from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLStackedWidget(QStackedWidget, QPSLWidgetBase):

    def __init__(self, parent: QWidget, object_name: str):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)