from QPSLClass.Base import *
from QPSLClass.QPSLObjectBase import QPSLObjectBase


class QPSLBoxLayoutBase(QPSLObjectBase):

    def __init__(self, parent: QWidget):
        super().__init__()
        self.m_widgets: List[QWidget] = []

    def add_widget(self, widget: QWidget):
        self.m_widgets.append(widget)
        QBoxLayout.addWidget(self, widget)

    def add_widgets(self, widgets: List[QWidget]):
        for widget in widgets:
            self.add_widget(widget=widget)

    def remove_widget(self, widget: QWidget):
        self.m_widgets.remove(widget)
        QBoxLayout.removeWidget(self, widget)

    def remove_widgets(self, widgets: List[QWidget]):
        for widget in widgets:
            self.remove_widget(widget=widget)

    def clear_widgets(self):
        for i in range(QBoxLayout.count(self) - 1, -1, -1):
            item: QLayoutItem = QBoxLayout.itemAt(self, i)
            if item.widget():
                item.widget().deleteLater()
            QBoxLayout.removeItem(self, item)
        self.m_widgets.clear()

    def set_stretch(self, sizes: Tuple[int, ...]):
        for i, size in enumerate(sizes):
            QBoxLayout.setStretch(self, i, size)

    def get_widget(self, index: int):
        return self.m_widgets[index]


class QPSLHBoxLayout(QHBoxLayout, QPSLBoxLayoutBase):

    def __init__(self,
                 parent: QWidget,
                 margins: Tuple[int, int, int, int] = (2, 2, 2, 2),
                 spacing: int = 5):
        super().__init__(parent=parent)
        QLayout.setContentsMargins(self, *margins)
        self.setSpacing(spacing)


class QPSLVBoxLayout(QVBoxLayout, QPSLBoxLayoutBase):

    def __init__(self,
                 parent: QWidget,
                 margins: Tuple[int, int, int, int] = (2, 2, 2, 2),
                 spacing: int = 5):
        super().__init__(parent=parent)
        QLayout.setContentsMargins(self, *margins)
        self.setSpacing(spacing)


class QPSLGridLayout(QGridLayout, QPSLObjectBase):

    def __init__(self,
                 parent: QWidget,
                 margins: Tuple[int, int, int, int] = (2, 2, 2, 2),
                 spacing: int = 5):
        super().__init__()
        self.m_widgets: List[QWidget] = []
        QGridLayout.setContentsMargins(self, *margins)
        self.setSpacing(spacing)

    def add_widget(self, widget: QWidget, start_row: int, end_row: int,
                   start_column: int, end_column: int):
        self.m_widgets.append(widget)
        QGridLayout.addWidget(self, widget, start_row, start_column,
                              end_row - start_row + 1,
                              end_column - start_column + 1)

    def add_widget_simple(self, widget: QWidget, grid: Tuple[int, int, int,
                                                             int]):
        self.add_widget(widget=widget,
                        start_row=grid[0],
                        end_row=grid[1],
                        start_column=grid[2],
                        end_column=grid[3])

    def remove_widget(self, widget: QWidget):
        self.m_widgets.remove(widget)
        QGridLayout.removeWidget(self, widget)

    def remove_widgets(self, widgets: List[QWidget]):
        for widget in widgets:
            self.remove_widget(widget=widget)

    def clear_widgets(self):
        for i in range(self.count() - 1, -1, -1):
            item: QLayoutItem = self.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            self.removeItem(item)
        self.m_widgets.clear()

    def get_widget(self, index: int):
        return self.m_widgets[index]

    def set_row_stretches(self, sizes: Tuple[int, ...]):
        for i, size in enumerate(sizes):
            self.setRowStretch(i, size)

    def set_column_stretches(self, sizes: Tuple[int, ...]):
        for i, size in enumerate(sizes):
            self.setColumnStretch(i, size)

    def set_stretch(self, row_sizes: Tuple[int, ...],
                    column_sizes: Tuple[int, ...]):
        self.set_row_stretches(sizes=row_sizes)
        self.set_column_stretches(sizes=column_sizes)


def QPSLBoxLayout(orientation: Qt.Orientation):
    if orientation == Qt.Orientation.Vertical:
        return QPSLVBoxLayout
    else:
        return QPSLHBoxLayout
