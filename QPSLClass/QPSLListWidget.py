from QPSLClass.Base import *
from QPSLClass.QPSLFrameBase import QPSLFrameBase


class QPSLTextListWidget(QListWidget, QPSLFrameBase):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 capacity: int = 100,
                 auto_scale: bool = True,
                 min_height=50,
                 unit_height=20,
                 max_height=120,
                 mode=QAbstractItemView.SelectionMode.SingleSelection,
                 scroll_mode=QAbstractItemView.ScrollMode.ScrollPerPixel,
                 frame_shape=QFrame.Shape.StyledPanel,
                 frame_shadow=QFrame.Shadow.Plain):
        super().__init__(parent=parent,
                         c_frame_shape=frame_shape,
                         c_frame_shadow=frame_shadow)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.m_capacity = capacity
        self.m_auto_scale = auto_scale
        self.m_min_height = min_height
        self.m_max_height = max_height
        self.m_unit_height = unit_height
        self.setSelectionMode(mode)
        self.setVerticalScrollMode(scroll_mode)
        self.scale_size()

    def set_auto_scale(self, auto_scale: bool):
        self.m_auto_scale = auto_scale

    def set_min_height(self, min_height: int):
        self.m_min_height = min_height

    def set_unit_height(self, unit_height: int):
        self.m_unit_height = unit_height

    def set_max_height(self, max_height: int):
        self.m_max_height = max_height

    def set_capacity(self, capacity: int):
        self.m_capacity = capacity
        if capacity:
            while self.count() >= self.m_capacity:
                self.removeItemWidget(self.takeItem(self))
        self.scrollToBottom(self)
        self.scale_size()

    def insert_item(self, row: int, text: str):
        if self.m_capacity and self.count() >= self.m_capacity:
            self.removeItemWidget(self.takeItem(0))
        self.insertItem(row, text)
        self.scale_size()

    def add_item(self, text: str):
        if self.m_capacity and self.count() >= self.m_capacity:
            self.removeItemWidget(self.takeItem(0))
        self.addItem(text)
        self.scale_size()

    def add_item_scroll(self, text: str):
        self.add_item(text=text)
        self.scrollToBottom()

    def remove_row(self, row: int):
        self.takeItem(row)
        self.scale_size()

    def remove_selected_item(self):
        self.takeItem(self.currentRow())
        self.scale_size()

    def clear(self):
        super().clear()
        self.scale_size()

    def scale_size(self):
        if not self.m_auto_scale:
            return
        if self.count() == 0:
            self.setFixedHeight(self.m_min_height)
        else:
            self.setFixedHeight(
                min(max(self.m_min_height,
                        self.count() * self.m_unit_height), self.m_max_height))
