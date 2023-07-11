from QPSLClass.Base import *
from QPSLClass.QPSLDockWidget import QPSLDockWidget
from QPSLClass.QPSLScrollList import QPSLHScrollList
from QPSLClass.QPSLPushButton import QPSLPushButton


class QPSLMenuDock(QPSLDockWidget):
    sig_show_up = pyqtSignal(QPSLDockWidget)
    sig_hide_up = pyqtSignal(QPSLDockWidget)
    sig_choose_module = pyqtSignal(str, str)

    def __init__(self, parent: QWidget, object_name: str, dir_name: str):
        super().__init__(parent=parent, object_name=object_name)
        self.m_dir = dir_name
        self.m_module_dict: Dict[str, str] = dict()
        self.set_widget(widget=QPSLHScrollList(
            self, object_name="{0}_box".format(object_name), fixed_height=100))
        self.setTitleBarWidget(QWidget())
        self.setFloating(True)
        self.setVisible(False)
        self.update_modules()

    @property
    def widget(self) -> QPSLHScrollList:
        return super().widget

    def update_modules(self):
        for dir in os.listdir("./%s" % self.m_dir):
            fullname = os.path.join("./%s" % self.m_dir, dir)
            if os.path.isdir(fullname) and "cache" not in dir:
                mod = str.split(dir, '.')[0]
                load_path = "{0}.{1}.{2}".format(self.m_dir, dir, dir)
                self.m_module_dict[mod] = load_path
        self.widget.clear_items()

    def choose_module(self, module_name: str):
        self.sig_choose_module.emit(module_name,
                                    self.m_module_dict[module_name])
        self.hide_menu()

    def show_menu(self):
        self.update_modules()
        for mod in self.m_module_dict:
            btn = QPSLPushButton(self.widget, object_name=mod, text=mod)
            btn.set_tooltip_enable()
            connect_direct(btn.sig_clicked[str], self.choose_module)
            self.widget.add_widget(widget=btn, ratio=2)
        self.setVisible(True)
        self.sig_show_up.emit(self)

    def hide_menu(self):
        self.setVisible(False)
        self.sig_hide_up.emit(self)

    def on_clicked(self):
        if self.isVisible():
            self.hide_menu()
        else:
            self.show_menu()
