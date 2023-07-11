from QPSLClass.Base import *
from QPSLClass.QPSLObjectBase import QPSLObjectBase


class QPSLProcess(QProcess, QPSLObjectBase):

    def __init__(self, parent: QWidget, qpsl_name: str):
        super(QPSLProcess, self).__init__(parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.set_object_name(name=qpsl_name)
