from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLMenuBar(QMenuBar, QPSLWidgetBase):

    def __init__(self, parent: QMainWindow, object_name: str):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)

    def add_menus(self, menus: List[QMenu]):
        for menu in menus:
            self.addMenu(menu)

    def add_actions(self, actions: List[QAction]):
        for act in actions:
            self.addAction(act)