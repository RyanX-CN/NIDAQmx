from QPSLClass.Base import *
from QPSLClass.QPSLLayout import QPSLHBoxLayout, QPSLVBoxLayout, QPSLBoxLayout, QPSLGridLayout
from QPSLClass.QPSLGroupBox import QPSLGroupBox


class QPSLGroupList(QPSLGroupBox):

    def setup(self, config: Dict):
        pass

    def remove_widget(self, widget: QWidget):
        self.layout.remove_widget(widget=widget)

    def remove_widgets(self, widgets: List[QWidget]):
        self.layout.remove_widgets(widgets=widgets)

    def clear_widgets(self):
        self.layout.clear_widgets()

    def get_widget(self, index: int):
        return self.layout.get_widget(index=index)

    def set_spacing(self, spacing: int):
        self.layout.setSpacing(spacing)

    @property
    def layout(self) -> Union[QPSLHBoxLayout, QPSLVBoxLayout, QPSLGridLayout]:
        return super().layout()


class QPSLLinearGroupList(QPSLGroupList):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 orientation: Qt.Orientation,
                 title: str = ""):
        super().__init__(parent=parent, object_name=object_name, title=title)
        self.setLayout(QPSLBoxLayout(orientation)(self))

    def add_widget(self, widget: QWidget):
        self.layout.add_widget(widget=widget)

    def add_widgets(self, widgets: List[QWidget]):
        self.layout.add_widgets(widgets=widgets)

    def set_stretch(self, sizes: Tuple[int, ...]):
        self.layout.set_stretch(sizes=sizes)

    @property
    def layout(self) -> Union[QPSLHBoxLayout, QPSLVBoxLayout]:
        return super().layout


class QPSLHorizontalGroupList(QPSLLinearGroupList):

    def __init__(self, parent: QWidget, object_name: str, title: str = ""):
        super().__init__(parent=parent,
                         object_name=object_name,
                         orientation=Qt.Orientation.Horizontal,
                         title=title)


class QPSLVerticalGroupList(QPSLLinearGroupList):

    def __init__(self, parent: QWidget, object_name: str, title: str = ""):
        super().__init__(parent=parent,
                         object_name=object_name,
                         orientation=Qt.Orientation.Vertical,
                         title=title)


class QPSLGridGroupList(QPSLGroupList):

    def __init__(self, parent: QWidget, object_name: str, title: str = ""):
        super().__init__(parent=parent, object_name=object_name, title=title)
        self.setLayout(QPSLGridLayout(self))

    def add_widget_simple(self, widget: QWidget, grid: Tuple[int, int, int,
                                                             int]):
        self.layout.add_widget_simple(widget=widget, grid=grid)

    def set_row_stretches(self, sizes: Tuple[int, ...]):
        self.layout.set_row_stretches(sizes=sizes)

    def set_column_stretches(self, sizes: Tuple[int, ...]):
        self.layout.set_column_stretches(sizes=sizes)

    def set_stretch(self, row_sizes: Tuple[int, ...],
                    column_sizes: Tuple[int, ...]):
        self.layout.set_stretch(row_sizes=row_sizes, column_sizes=column_sizes)

    @property
    def layout(self) -> QPSLGridLayout:
        return super().layout
