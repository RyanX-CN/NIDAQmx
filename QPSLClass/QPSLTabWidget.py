from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLTabWidget(QTabWidget, QPSLWidgetBase):
    sig_tab_raised = pyqtSignal([int], [str], [QWidget])

    def __init__(self, parent: QWidget, object_name: str):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.m_tabs: List[QWidget] = []
        connect_direct(self.currentChanged, self.on_current_changed)

    def add_tab(self, tab: QWidget, title: str):
        self.addTab(tab, title)
        self.m_tabs.append(tab)

    def insert_tab(self, tab: QWidget, title: str, index: int):
        self.insertTab(index, tab, title)
        self.m_tabs.insert(index, tab)

    def remove_tab(self, tab: QWidget):
        self.removeTab(self.indexOf(tab))
        self.m_tabs.remove(tab)

    def get_tab(self, index: int):
        return self.m_tabs[index]

    def on_current_changed(self, index: int):
        self.sig_tab_raised[int].emit(self.currentIndex())
        self.sig_tab_raised[str].emit(self.current_tab_label())
        self.sig_tab_raised[QWidget].emit(self.currentWidget())

    def current_tab_label(self):
        return self.tabText(self.currentIndex())

    def current_widget(self):
        return self.currentWidget()
