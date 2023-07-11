from QPSLClass.Base import *
from QPSLClass.QPSLGroupList import QPSLHorizontalGroupList
from QPSLClass.QPSLRangeBox import QPSLRangeBox, QPSLFloatRangeBox
from QPSLClass.QPSLSpinBox import QPSLSpinBox
from QPSLClass.QPSLCheckBoxGroup import QPSLCheckBox


class QPSLRangeTaskBox(QPSLHorizontalGroupList):
    sig_value_changed = pyqtSignal()

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 min: int,
                 max: int,
                 step_num: int,
                 stretch: Tuple[int, int, int] = (4, 2, 1),
                 title: str = ""):
        super().__init__(parent=parent, object_name=object_name, title=title)
        self.add_widget(widget=QPSLRangeBox(
            self, object_name="box_range", min=min, max=max))
        self.add_widget(widget=QPSLSpinBox(self,
                                           object_name="spin_step_num",
                                           min=1,
                                           max=1000,
                                           value=step_num,
                                           prefix="step num:"))
        self.add_widget(widget=QPSLCheckBox(
            self, object_name="check_box", text="end-point"))
        self.set_stretch(sizes=stretch)
        connect_direct(self.box_range.spin_min.valueChanged,
                       self.sig_value_changed)
        connect_direct(self.box_range.spin_max.valueChanged,
                       self.sig_value_changed)
        connect_direct(self.spin_step_num.valueChanged, self.sig_value_changed)
        connect_direct(self.spin_step_num.valueChanged, self.sig_value_changed)

    def get_interval_length(self):
        return (self.box_range.spin_max.value() -
                self.box_range.spin_min.value()) // (
                    self.spin_step_num.value() -
                    self.check_box_end_point.isChecked())

    @property
    def box_range(self) -> QPSLRangeBox:
        return self.get_widget(0)

    @property
    def spin_step_num(self) -> QPSLSpinBox:
        return self.get_widget(1)

    @property
    def check_box_end_point(self) -> QPSLCheckBox:
        return self.get_widget(2)


class QPSLFloatRangeTaskBox(QPSLHorizontalGroupList):
    sig_value_changed = pyqtSignal()

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 min: int,
                 max: int,
                 step_num: int,
                 stretch: Tuple[int, int, int] = (4, 2, 1),
                 title: str = ""):
        super().__init__(parent=parent, object_name=object_name, title=title)
        self.add_widget(widget=QPSLFloatRangeBox(
            self, object_name="box_range", min=min, max=max))
        self.add_widget(widget=QPSLSpinBox(self,
                                           object_name="spin_step_num",
                                           min=1,
                                           max=1000,
                                           value=step_num,
                                           prefix="step num:"))
        self.add_widget(widget=QPSLCheckBox(
            self, object_name="check_box", text="end-point"))
        self.set_stretch(sizes=stretch)
        connect_direct(self.box_range.spin_min.valueChanged,
                       self.sig_value_changed)
        connect_direct(self.box_range.spin_max.valueChanged,
                       self.sig_value_changed)
        connect_direct(self.spin_step_num.valueChanged, self.sig_value_changed)
        connect_direct(self.spin_step_num.valueChanged, self.sig_value_changed)

    def get_interval_length(self):
        return (
            self.box_range.spin_max.value() - self.box_range.spin_min.value()
        ) / (self.spin_step_num.value() - self.check_box_end_point.isChecked())

    def get_values(self) -> np.ndarray:
        return np.linspace(start=self.box_range.spin_min.value(),
                           stop=self.box_range.spin_max.value(),
                           num=self.spin_step_num.value(),
                           endpoint=self.check_box_end_point.isChecked())

    @property
    def box_range(self) -> QPSLFloatRangeBox:
        return self.get_widget(0)

    @property
    def spin_step_num(self) -> QPSLSpinBox:
        return self.get_widget(1)

    @property
    def check_box_end_point(self) -> QPSLCheckBox:
        return self.get_widget(2)
