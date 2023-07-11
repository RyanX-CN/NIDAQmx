from QPSLClass.Base import *
from QPSLClass.QPSLGroupList import QPSLHorizontalGroupList
from QPSLClass.QPSLSlider import QPSLSlider, QPSLFloatSlider
from QPSLClass.QPSLSpinBox import QPSLSpinBox, QPSLDoubleSpinBox


class QPSLRangeBox(QPSLHorizontalGroupList):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 min: int,
                 max: int,
                 value: Optional[int] = None,
                 title=""):
        super().__init__(parent=parent, object_name=object_name, title=title)
        self.add_widget(widget=QPSLSpinBox(
            self, object_name="spin_min", min=min, max=max, value=min))
        if value is not None:
            self.add_widget(
                widget=QPSLSlider(self,
                                  object_name="slider",
                                  orientation=Qt.Orientation.Horizontal,
                                  min=min,
                                  max=max,
                                  value=value))
            self.slider.setSizePolicy(QSizePolicy.Policy.Expanding,
                                      QSizePolicy.Policy.Expanding)
        self.add_widget(widget=QPSLSpinBox(
            self, object_name="spin_max", min=min, max=max, value=max))

    @property
    def spin_min(self) -> QPSLSpinBox:
        return self.get_widget(0)

    @property
    def slider(self) -> QPSLSlider:
        return self.get_widget(1)

    @property
    def spin_max(self) -> QPSLSpinBox:
        return self.get_widget(-1)


class QPSLFloatRangeBox(QPSLHorizontalGroupList):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 min: float,
                 max: float,
                 value: Optional[float] = None,
                 decimals: int = 3,
                 title=""):
        super().__init__(parent=parent, object_name=object_name, title=title)
        self.add_widget(widget=QPSLDoubleSpinBox(self,
                                                 object_name="spin_min",
                                                 min=min,
                                                 max=max,
                                                 value=min,
                                                 decimals=decimals))
        if value is not None:
            self.add_widget(
                widget=QPSLFloatSlider(self,
                                       object_name="slider",
                                       orientation=Qt.Orientation.Horizontal,
                                       min=min,
                                       max=max,
                                       value=value,
                                       decimals=decimals))
            self.slider.setSizePolicy(QSizePolicy.Policy.Expanding,
                                      QSizePolicy.Policy.Expanding)
        self.add_widget(widget=QPSLDoubleSpinBox(self,
                                                 object_name="spin_max",
                                                 min=min,
                                                 max=max,
                                                 value=max,
                                                 decimals=decimals))

    @property
    def spin_min(self) -> QPSLDoubleSpinBox:
        return self.get_widget(0)

    @property
    def slider(self) -> QPSLFloatSlider:
        return self.get_widget(1)

    @property
    def spin_max(self) -> QPSLDoubleSpinBox:
        return self.get_widget(-1)
