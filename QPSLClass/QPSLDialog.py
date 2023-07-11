from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLDialogButtonBox(QDialogButtonBox, QPSLWidgetBase):

    def __init__(
        self,
        parent: QWidget,
        object_name: str,
        buttons: Union[QDialogButtonBox.StandardButton, QDialogButtonBox.
                       StandardButtons] = QDialogButtonBox.StandardButton.Ok):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.setStandardButtons(buttons)


class QPSLDialog(QDialog, QPSLWidgetBase):
    sig_close = pyqtSignal()

    def __init__(self, parent: QWidget, object_name: str, window_title: str):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.setWindowTitle(window_title)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.sig_close.emit()
        return super().closeEvent(a0)
