from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLScrollArea(QScrollArea, QPSLWidgetBase):

    def __init__(self, parent: QWidget, object_name: str,
                 orientation: Qt.Orientation):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)


class QPSLHScrollArea(QPSLScrollArea):

    def __init__(self, parent: QWidget, object_name: str):
        super().__init__(parent=parent,
                         object_name=object_name,
                         orientation=Qt.Orientation.Horizontal)


class QPSLVScrollArea(QPSLScrollArea):

    def __init__(self, parent: QWidget, object_name: str):
        super().__init__(parent=parent,
                         object_name=object_name,
                         orientation=Qt.Orientation.Vertical)
