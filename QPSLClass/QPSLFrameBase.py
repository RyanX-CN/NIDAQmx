from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLFrameBase(QPSLWidgetBase):

    def __init__(self,
                 c_frame_shape=QFrame.Shape.StyledPanel,
                 c_frame_shadow=QFrame.Shadow.Plain):
        super().__init__()
        QFrame.setFrameShape(self, c_frame_shape)
        QFrame.setFrameShadow(self, c_frame_shadow)
