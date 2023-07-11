from QPSLClass.Base import *
from QPSLClass.QPSLFrameBase import QPSLFrameBase


class QPSLSplitter(QSplitter, QPSLFrameBase):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 orientation: Qt.Orientation,
                 frame_shape: QFrame.Shape = QFrame.Shape.StyledPanel,
                 frame_shadow: QFrame.Shadow = QFrame.Shadow.Plain):
        super().__init__(parent=parent,
                         orientation=orientation,
                         c_frame_shape=frame_shape,
                         c_frame_shadow=frame_shadow)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)

    def add_widgets(self, widgets: List[QWidget]):
        for widget in widgets:
            self.addWidget(widget)

    def remove_widget(self, widget: QWidget):
        widget.setParent(None)

    def get_widgets(self):
        return [self.widget(i) for i in range(self.count())]

    def set_widgets(self, widgets: List[QWidget]):
        self.clear_widgets()
        self.add_widgets(widgets=widgets)

    def clear_widgets(self):
        widgets = [self.widget(i) for i in range(self.count())]
        for widget in widgets:
            self.remove_widget(widget=widget)


class QPSLHSplitter(QPSLSplitter):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 frame_shape: QFrame.Shape = QFrame.Shape.StyledPanel,
                 frame_shadow: QFrame.Shadow = QFrame.Shadow.Plain):
        super().__init__(parent=parent,
                             object_name=object_name,
                             orientation=Qt.Orientation.Horizontal,
                             frame_shape=frame_shape,
                             frame_shadow=frame_shadow)


class QPSLVSplitter(QPSLSplitter):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 frame_shape: QFrame.Shape = QFrame.Shape.StyledPanel,
                 frame_shadow: QFrame.Shadow = QFrame.Shadow.Plain):
        super().__init__(parent=parent,
                             object_name=object_name,
                             orientation=Qt.Orientation.Vertical,
                             frame_shape=frame_shape,
                             frame_shadow=frame_shadow)
