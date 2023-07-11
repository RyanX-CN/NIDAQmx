from QPSLClass.Base import *
from QPSLClass.QPSLObjectBase import QPSLObjectBase


class QPSLShortCut(QShortcut, QPSLObjectBase):

    def __init__(self, key: str, parent: QWidget,
                 callback: Union[Callable[..., None],
                                 pyqtBoundSignal], object_name: str):
        super().__init__(key, parent, callback)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)