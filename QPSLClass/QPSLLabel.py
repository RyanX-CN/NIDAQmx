from QPSLClass.Base import *
from QPSLClass.QPSLFrameBase import QPSLFrameBase


class QPSLLabel(QLabel, QPSLFrameBase):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 text: str = "",
                 frame_shape: QFrame.Shape = QFrame.Shape.StyledPanel,
                 frame_shadow: QFrame.Shadow = QFrame.Shadow.Plain):
        super().__init__(parent=parent,
                         c_frame_shape=frame_shape,
                         c_frame_shadow=frame_shadow)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.setText(text)


class QPSLTextLabel(QPSLLabel):

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
        self.set_text(text)

    def set_text(self, text: str):
        self.m_text = text
        self.update_text(text)
        self.update_tooltip()

    def set_font(self, font: QFont):
        super().setFont(font)
        self.update_text(text=self.m_text)

    def text(self):
        return self.m_text

    def update_text(self, text: str):
        w = self.fontMetrics().width(text)
        if w > self.width():
            self.setText(self.fontMetrics().elidedText(
                text, Qt.TextElideMode.ElideRight, self.width()))
        else:
            self.setText(text)

    def update_tooltip(self):
        if self.m_tooltip_enable:
            self.setToolTip(self.text())
        else:
            self.setToolTip("")


class QPSLScalePixmapLabel(QPSLLabel):

    sig_touch = pyqtSignal([], [QLabel], [QPixmap])

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
                 frame_shape: QFrame.Shape = QFrame.Shape.StyledPanel,
                 frame_shadow: QFrame.Shadow = QFrame.Shadow.Plain):
        super().__init__(parent=parent,
                         object_name=object_name,
                         text="",
                         frame_shape=frame_shape,
                         frame_shadow=frame_shadow)
        self.m_pixmap: QPixmap = None
        self.m_aspect_ratio_mode = Qt.AspectRatioMode.KeepAspectRatio
        self.m_aspect_ratio_mode_callbacks: List[Callable] = []
        self.setAlignment(alignment)
        self.setSizePolicy(QSizePolicy.Policy.Ignored,
                           QSizePolicy.Policy.Ignored)
        self.m_aspect_ratio_mode_callbacks.append(
            self.add_context_actions_single_choice(
                ["KeepAspectRatio", "IgnoreAspectRatio"],
                "AspectRatioMode",
                callback=self.set_aspect_ratio_mode))

    def set_pixmap(self, pixmap: QPixmap):
        self.m_pixmap = pixmap
        self.setPixmap(
            pixmap.scaled(self.width(), self.height(),
                          self.m_aspect_ratio_mode))

    def set_aspect_ratio_mode(self, mode: Union[Qt.AspectRatioMode, str]):
        if mode == "KeepAspectRatio" or mode == Qt.AspectRatioMode.KeepAspectRatio:
            mode = "KeepAspectRatio"
            self.m_aspect_ratio_mode = Qt.AspectRatioMode.KeepAspectRatio
        elif mode == "IgnoreAspectRatio" or mode == Qt.AspectRatioMode.IgnoreAspectRatio:
            mode = "IgnoreAspectRatio"
            self.m_aspect_ratio_mode = Qt.AspectRatioMode.IgnoreAspectRatio
        for callback in self.m_aspect_ratio_mode_callbacks:
            callback(mode)
        self.setPixmap(
            self.m_pixmap.scaled(self.width(), self.height(),
                                 self.m_aspect_ratio_mode))

    def resizeEvent(self, a0: QResizeEvent):
        if self.m_pixmap:
            self.setPixmap(
                self.m_pixmap.scaled(self.width(), self.height(),
                                     self.m_aspect_ratio_mode))
        return super().resizeEvent(a0)

    def mousePressEvent(self, ev: QMouseEvent):
        self.sig_touch.emit()
        self.sig_touch[QLabel].emit(self)
        if self.m_pixmap:
            self.sig_touch[QPixmap].emit(self.m_pixmap)
        self.sig_touch.emit()

        return super().mousePressEvent(ev)