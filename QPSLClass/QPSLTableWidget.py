from QPSLClass.Base import *
from QPSLClass.QPSLFrameBase import QPSLFrameBase


class QPSLTableWidget(QTableWidget, QPSLFrameBase):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 frame_shape: QFrame.Shape = QFrame.Shape.StyledPanel,
                 frame_shadow: QFrame.Shadow = QFrame.Shadow.Plain):
        super().__init__(parent=parent,
                                              c_frame_shape=frame_shape,
                                              c_frame_shadow=frame_shadow)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)