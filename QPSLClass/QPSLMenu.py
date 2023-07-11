from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLMenu(QMenu, QPSLWidgetBase):

    def __init__(self, parent: QMenuBar, object_name: str, title: str):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.setTitle(title)

    def add_actions(self, actions: List[QAction]):
        for action in actions:
            self.addAction(action)