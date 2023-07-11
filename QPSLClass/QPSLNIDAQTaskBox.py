from QPSLClass.Base import *
from QPSLClass.QPSLGroupList import QPSLGridGroupList
from QPSLClass.QPSLComboBox import QPSLFreshTextComboBox
from QPSLClass.QPSLSpinBox import QPSLSpinBox
from QPSLClass.QPSLPushButton import QPSLPushButton


class QPSLNIDAQTaskBox(QPSLGridGroupList):

    def __init__(self, parent: QWidget, object_name: str, title: str = ""):
        super().__init__(parent=parent, object_name=object_name, title=title)
        self.add_widget_simple(widget=QPSLFreshTextComboBox(
            self, object_name="cbox_device", text="device:"),
                               grid=(0, 0, 0, 0))
        self.add_widget_simple(widget=QPSLFreshTextComboBox(
            self, object_name="cbox_terminal", text="terminal:"),
                               grid=(0, 0, 1, 1))
        self.add_widget_simple(widget=QPSLSpinBox(
            self,
            object_name="spin_sample_rate",
            min=1,
            max=20000000,
            value=1000,
            prefix="sample rate:",
            suffix="/s"),
                               grid=(1, 1, 0, 0))
        self.add_widget_simple(widget=QPSLSpinBox(
            self,
            object_name="spin_sample_number",
            min=0,
            max=20000000,
            value=0,
            prefix="sample number:"),
                               grid=(1, 1, 1, 1))
        self.spin_sample_number.setSpecialValueText("sample mode: continuous")

    @property
    def cbox_device(self) -> QPSLFreshTextComboBox:
        return self.get_widget(0)

    @property
    def cbox_terminal(self) -> QPSLFreshTextComboBox:
        return self.get_widget(1)

    @property
    def spin_sample_rate(self) -> QPSLSpinBox:
        return self.get_widget(2)

    @property
    def spin_sample_number(self) -> QPSLSpinBox:
        return self.get_widget(3)

    @property
    def cboxes(self) -> Iterable[QPSLFreshTextComboBox]:
        return (self.cbox_device, self.cbox_terminal)

    @property
    def push_buttons(self) -> Iterable[QPSLPushButton]:
        yield from map(lambda w: w.btn_fresh, self.cboxes)

    @property
    def spins(self) -> Iterable[QPSLSpinBox]:
        return (self.spin_sample_rate, self.spin_sample_number)
