from QPSLClass.Base import *
from QPSLClass.QPSLObjectBase import QPSLObjectBase


class QPSLAction(QAction, QPSLObjectBase):

    def __init__(self,
                 parent: QMenuBar,
                 object_name: str,
                 text: str,
                 checkable: bool,
                 checked=False):

        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.setText(text)
        self.setCheckable(checkable)
        self.setChecked(checked)
        