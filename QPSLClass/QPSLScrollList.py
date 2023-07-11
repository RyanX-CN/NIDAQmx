from QPSLClass.Base import *
from QPSLClass.QPSLGroupList import QPSLLinearGroupList
from QPSLClass.QPSLScrollArea import QPSLScrollArea


class QPSLScrollList(QPSLScrollArea):

    def __init__(self, parent: QWidget, object_name: str, fixed_length: int,
                 orientation: Qt.Orientation):
        super().__init__(parent=parent,
                         object_name=object_name,
                         orientation=orientation)
        self.m_items: List[Tuple[QWidget, float]] = []
        self.m_fixed_length = fixed_length
        self.m_orientation = orientation
        self.setWidget(
            QPSLLinearGroupList(self, object_name="widget", orientation=orientation))

    @property
    def widget(self) -> QPSLLinearGroupList:
        return super().widget()

    @property
    def scrollBar(self):
        if self.m_orientation == Qt.Orientation.Horizontal:
            return self.horizontalScrollBar()
        else:
            return self.verticalScrollBar()

    def add_widget(self, widget: QWidget, ratio: float):
        self.m_items.append((widget, ratio))
        self.widget.add_widget(widget=widget)
        self.update_item_size(widget=widget, ratio=ratio)
        self.update_size()

    def get_space_without_scrollbar(self):
        return 8 + self.get_extra_space()

    def get_extra_space(self):
        return 4

    def update_size(self):
        layout = self.widget.layout
        l, t, r, b = layout.getContentsMargins()
        minh, minw = 0, 0
        if self.m_orientation == Qt.Orientation.Horizontal:
            if self.m_items:
                minw += (len(self.m_items) - 1) * layout.spacing()
            for w, r in self.m_items:
                minh = max(minh, w.height())
                minw += w.width()
            self.widget.setFixedSize(minw + l + r,
                                     minh + r + b + self.get_extra_space())
            if self.scrollBar.isVisible():
                self.setFixedHeight(self.m_fixed_length +
                                    self.scrollBar.height())
            else:
                self.setFixedHeight(self.m_fixed_length)
        else:
            if self.m_items:
                minh += (len(self.m_items) - 1) * layout.spacing()
            for w, r in self.m_items:
                minh += w.height()
                minw = max(minw, w.width())
            self.widget.setFixedSize(minw + l + r + self.get_extra_space(),
                                     minh + r + b)
            if self.scrollBar.isVisible():
                self.setFixedWidth(self.m_fixed_length +
                                   self.scrollBar.width())
            else:
                self.setFixedWidth(self.m_fixed_length)

    def update_item_size(self, widget: QWidget, ratio: float):
        if self.m_orientation == Qt.Orientation.Horizontal:
            widget.setFixedSize(
                int(ratio * (self.m_fixed_length -
                             self.get_space_without_scrollbar())),
                self.m_fixed_length - self.get_space_without_scrollbar())
        else:
            widget.setFixedSize(
                self.m_fixed_length - self.get_space_without_scrollbar(),
                int(ratio * (self.m_fixed_length -
                             self.get_space_without_scrollbar())))

    def update_items_size(self):
        for w, r in self.m_items:
            self.update_item_size(widget=w, ratio=r)

    def clear_items(self):
        self.widget.clear_widgets()
        self.m_items.clear()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.update_items_size()
        self.update_size()
        return super().resizeEvent(a0)

    def showEvent(self, a0) -> None:
        self.update_items_size()
        self.update_size()
        return super().showEvent(a0)


class QPSLHScrollList(QPSLScrollList):

    def __init__(self, parent: QWidget, object_name: str, fixed_height: int):
        super().__init__(parent=parent,
                         object_name=object_name,
                         fixed_length=fixed_height,
                         orientation=Qt.Orientation.Horizontal)


class QPSLVScrollList(QPSLScrollList):

    def __init__(self, parent: QWidget, object_name: str, fixed_width: int):
        super().__init__(parent=parent,
                         object_name=object_name,
                         fixed_length=fixed_width,
                         orientation=Qt.Orientation.Vertical)
