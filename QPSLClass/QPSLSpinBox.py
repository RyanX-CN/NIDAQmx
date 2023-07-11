from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLSpinBox(QSpinBox, QPSLWidgetBase):
    sig_editing_finished = pyqtSignal([], [int])

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 min: int = -1000000,
                 max: int = 1000000,
                 value: int = 0,
                 prefix: str = "",
                 suffix: str = ""):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.setRange(min, max)
        self.setValue(value)
        self.setPrefix(prefix)
        self.setSuffix(suffix)
        connect_direct(self.editingFinished, self.on_editing_finished)

    def set_read_only(self, b: bool):
        self.setReadOnly(b)
        if b:
            self.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        else:
            self.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)

    def on_editing_finished(self):
        self.sig_editing_finished.emit()
        self.sig_editing_finished[int].emit(self.value())

    def edit_value(self, value: int):
        self.setValue(value)
        self.sig_editing_finished.emit()
        self.sig_editing_finished[int].emit(self.value())


class QPSLDoubleSpinBox(QDoubleSpinBox, QPSLWidgetBase):
    sig_editing_finished = pyqtSignal([], [float])

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 min: float = -1000000.0,
                 max: float = 1000000.0,
                 value: float = 0,
                 prefix: str = "",
                 suffix: str = "",
                 decimals: int = 3):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.setDecimals(decimals)
        self.setRange(min, max)
        self.setValue(value)
        self.setPrefix(prefix)
        self.setSuffix(suffix)
        connect_direct(self.editingFinished, self.on_editing_finished)

    def set_read_only(self, b: bool):
        self.setReadOnly(b)
        if b:
            self.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        else:
            self.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.UpDownArrows)

    def on_editing_finished(self):
        self.sig_editing_finished.emit()
        self.sig_editing_finished[float].emit(self.value())

    def edit_value(self, value: float):
        self.setValue(value)
        self.sig_editing_finished.emit()
        self.sig_editing_finished[float].emit()
