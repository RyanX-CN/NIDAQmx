from QPSLClass.Base import *
from QPSLClass.QPSLLabel import QPSLLabel, QPSLScalePixmapLabel


class QPSLTrackedLabel(QPSLLabel):
    sig_mouse_click = pyqtSignal(QPointF)
    sig_mouse_hover = pyqtSignal(QPointF)

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 text: str = "",
                 frame_shape: QFrame.Shape = QFrame.Shape.StyledPanel,
                 frame_shadow: QFrame.Shadow = QFrame.Shadow.Plain):
        super().__init__(parent=parent,
                         object_name=object_name,
                         text=text,
                         frame_shape=frame_shape,
                         frame_shadow=frame_shadow)
        self.setMouseTracking(True)

    def convert_position_to_ratio(self, pos: QPoint):
        x = pos.x() / self.width()
        y = pos.y() / self.height()
        return QPointF(x, y)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = self.convert_position_to_ratio(pos=event.pos())
            self.sig_mouse_click.emit(pos)
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = self.convert_position_to_ratio(pos=event.pos())
        self.sig_mouse_hover.emit(pos)
        return super().mouseMoveEvent(event)


class QPSLTrackedScalePixmapLabel(QPSLScalePixmapLabel):
    sig_mouse_click = pyqtSignal(QPointF)
    sig_mouse_hover = pyqtSignal(QPointF)

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
                 frame_shape: QFrame.Shape = QFrame.Shape.StyledPanel,
                 frame_shadow: QFrame.Shadow = QFrame.Shadow.Plain):
        super().__init__(parent=parent,
                         object_name=object_name,
                         alignment=alignment,
                         frame_shape=frame_shape,
                         frame_shadow=frame_shadow)
        self.setMouseTracking(True)

    def convert_position_to_ratio(self, pos: QPoint):
        x = pos.x() / self.width()
        y = pos.y() / self.height()
        return QPointF(x, y)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = self.convert_position_to_ratio(pos=event.pos())
            self.sig_mouse_click.emit(pos)
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = self.convert_position_to_ratio(pos=event.pos())
        self.sig_mouse_hover.emit(pos)
        return super().mouseMoveEvent(event)