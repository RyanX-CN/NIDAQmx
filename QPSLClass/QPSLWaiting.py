from QPSLClass.Base import *
from QPSLClass.QPSLLabel import QPSLLabel
from QPSLClass.QPSLLayout import QPSLGridLayout
from QPSLClass.QPSLDialog import QPSLDialog


class QPSLWaitingLabel(QPSLLabel):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 size: QSize,
                 speed: int = 200,
                 frame_shape: QFrame.Shape = QFrame.Shape.NoFrame,
                 frame_shadow: QFrame.Shadow = QFrame.Shadow.Plain):
        super().__init__(parent=parent,
                         object_name=object_name,
                         text="",
                         frame_shape=frame_shape,
                         frame_shadow=frame_shadow)
        self.resize(size)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMovie(QMovie("resources/loading.gif"))
        self.movie().setScaledSize(size)
        self.movie().setCacheMode(QMovie.CacheMode.CacheAll)
        self.set_speed(speed=speed)

    def get_speed(self):
        return self.movie().speed()

    def set_speed(self, speed):
        self.movie().setSpeed(speed)

    def start_movie(self):
        self.movie().start()

    def stop_movie(self):
        self.movie().stop()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.movie().setScaledSize(a0.size())
        return super().resizeEvent(a0)


class QPSLWaitingDialog(QPSLDialog):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 size: QSize,
                 speed: int = 200):
        super().__init__(parent=parent,
                         object_name=object_name,
                         window_title="")

        self.resize(size)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint
                            | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setLayout(QPSLGridLayout(self))
        self.layout.add_widget_simple(widget=QPSLLabel(
            self, object_name="label", frame_shape=QFrame.Shape.NoFrame),
                                      grid=(0, 0, 0, 0))
        self.label.setMovie(QMovie("resources/loading.gif"))
        self.label.movie().setScaledSize(size)
        self.label.movie().setCacheMode(QMovie.CacheMode.CacheAll)
        self.set_speed(speed=speed)
        self.start_movie()

    @property
    def layout(self) -> QPSLGridLayout:
        return super().layout()

    @property
    def label(self) -> QPSLLabel:
        return self.layout.get_widget(0)

    def get_speed(self):
        return self.label.movie().speed()

    def set_speed(self, speed):
        self.label.movie().setSpeed(speed)

    def start_movie(self):
        self.label.movie().start()

    def stop_movie(self):
        self.label.movie().stop()