from QPSLClass.Base import *
from QPSLClass.QPSLObjectBase import QPSLObjectBase


class QPSLThread(QThread, QPSLObjectBase):

    def __init__(self, parent: QObject, object_name: str):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)