from QPSLClass.Base import *
from QPSLClass.QPSLObjectBase import QPSLObjectBase


class QPSLBool(QObject, QPSLObjectBase):
    __slots__ = "m_val"
    sig_value_changed = pyqtSignal(bool)

    def __init__(self, val=False):
        super().__init__()
        self.m_val = val

    def set_value(self, val: bool):
        if val != self.m_val:
            changed = True
        self.m_val = val
        if changed:
            self.sig_value_changed.emit(val)

    def get_value(self):
        return self.m_val

    def __bool__(self):
        return self.m_val