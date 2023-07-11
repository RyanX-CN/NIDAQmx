from QPSLClass.Base import *
from QPSLClass.QPSLWidget import QPSLWidget
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLDockWidget(QDockWidget, QPSLWidgetBase):
    sig_dockwidget_closed = pyqtSignal([], [QDockWidget])

    def __init__(self, parent: QWidget, object_name: str):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint
                            | Qt.WindowType.WindowCloseButtonHint)

    @property
    def widget(self) -> QPSLWidget:
        return super().widget()

    def set_widget(self, widget: QPSLWidget):
        self.setWidget(widget)

    def closeEvent(self, event: QCloseEvent):
        if self.widget is not None:
            self.widget.to_delete()
        self.sig_dockwidget_closed.emit()
        self.sig_dockwidget_closed[QDockWidget].emit(self)
        return super().closeEvent(event)
