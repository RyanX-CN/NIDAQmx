from QPSLClass.Base import *
from QPSLClass.QPSLGroupList import QPSLHorizontalGroupList, QPSLVerticalGroupList
from QPSLClass.QPSLComboBox import QPSLFreshTextComboBox
from QPSLClass.QPSLSpinBox import QPSLDoubleSpinBox


class QPSLNIDAQChannelBox(QPSLVerticalGroupList):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 title: str = "",
                 text="channel:"):
        super().__init__(parent=parent, object_name=object_name, title=title)
        self.add_widget(widget=QPSLFreshTextComboBox(
            self, object_name="cbox_channel", text=text))
        self.add_widget(widget=QPSLHorizontalGroupList(self, object_name="box_range"))
        self.box_range.add_widget(
            widget=QPSLDoubleSpinBox(self.box_range,
                                     object_name="spin_min",
                                     min=-10,
                                     max=10,
                                     value=0,
                                     prefix="min:"))
        self.spin_min.set_read_only(True)
        self.box_range.add_widget(
            widget=QPSLDoubleSpinBox(self.box_range,
                                     object_name="spin_max",
                                     min=-10,
                                     max=3.3,
                                     value=10,
                                     prefix="max:"))
        self.spin_max.set_read_only(True)

    @property
    def cbox_channel(self) -> QPSLFreshTextComboBox:
        return self.get_widget(0)

    @property
    def box_range(self) -> QPSLHorizontalGroupList:
        return self.get_widget(1)

    @property
    def spin_min(self) -> QPSLDoubleSpinBox:
        return self.box_range.get_widget(0)

    @property
    def spin_max(self) -> QPSLDoubleSpinBox:
        return self.box_range.get_widget(1)