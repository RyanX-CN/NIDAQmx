from QPSLClass.Base import *
from QPSLClass.QPSLMainWindow import QPSLMainWindow
from QPSLClass.QPSLMenuBar import QPSLMenuBar
from QPSLClass.QPSLMenuDock import QPSLMenuDock
from QPSLClass.QPSLWidget import QPSLWidget


class QPSLStartWindow(QPSLMainWindow):

    def __init__(self,
                 object_name="window",
                 window_title="QPSL-pyQt-8.0") -> None:
        super().__init__(parent=None, object_name=object_name)
        self.m_is_single_plugin = configer_getset("is_single_plugin", False)
        self.m_active_menudock = None
        self.setWindowTitle(window_title)
        if self.m_is_single_plugin:
            self.m_single_plugin_name = configer_get("single_plugin_name")
            self.set_single_plugin_central_widget(
                self.m_single_plugin_name,
                "Plugins.{0}.{0}".format(self.m_single_plugin_name))
        else:
            self.resize(1000, 500)
            self.setMenuBar(QPSLMenuBar(self, object_name="menubar"))
            self.add_plugin_action_menu(action_name="python plugins",
                                        dir_name="Plugins")
            # self.add_plugin_action_menu(action_name="external plugins",
            #                             dir_name="Externals")
            # self.add_plugin_action_menu(action_name="combined plugins",
            #                             dir_name="Combines")
            self.add_context_action_menu()
            self.add_virtual_mode_choice()
            connect_direct(self.settings_menu.aboutToShow,
                           self.hide_active_menudock)

    def add_plugin_action_menu(self, action_name: str, dir_name: str):
        menudock = QPSLMenuDock(self,
                                object_name=action_name,
                                dir_name=dir_name)
        self.m_menudocks[action_name] = menudock
        connect_direct(menudock.sig_show_up, self.on_menudock_show_up)
        connect_direct(menudock.sig_hide_up, self.on_menudock_hide_up)
        connect_direct(menudock.sig_choose_module, self.on_module_clicked)
        connect_direct(
            self.add_action(action_name=action_name).triggered,
            menudock.on_clicked)

    def on_menudock_show_up(self, menudock: QPSLMenuDock):
        self.hide_active_menudock()
        self.m_active_menudock = menudock
        self.update_menudock_size()
        self.update_menudock_position()

    def on_menudock_hide_up(self, menudock: QPSLMenuDock):
        if self.m_active_menudock == menudock:
            self.m_active_menudock = None

    def hide_active_menudock(self):
        if self.m_active_menudock:
            self.m_active_menudock.hide_menu()

    def on_module_clicked(self, mod: str, path: str):
        self.add_debug(msg="load module {0} ...".format(mod))
        _class = getattr(importlib.import_module(path), "MainWidget")
        widget: QPSLWidget = _class(None,
                                    virtual_mode=bool(self.m_virtual_mode))
        dock_widget = self.add_dockwidget(widget=widget)
        dock_widget.show()
        dock_widget.raise_()
        connect_direct(dock_widget.sig_dockwidget_closed,
                       self.sig_dockwidget_closed)
        connect_direct(dock_widget.sig_dockwidget_closed[QDockWidget],
                       self.sig_dockwidget_closed[QDockWidget])
        return dock_widget

    def update_menudock_size(self):
        self.m_active_menudock: QPSLMenuDock
        self.m_active_menudock.resize(self.width(),
                                      self.m_active_menudock.height())

    def update_menudock_position(self):
        self.m_active_menudock: QPSLMenuDock
        self.m_active_menudock.move(
            self.menu_bar.mapToGlobal(self.menu_bar.rect().bottomLeft()))

    def set_single_plugin_central_widget(self, mod: str, path: str):
        self.add_debug(msg="load module {0} ...".format(mod))
        _class = getattr(importlib.import_module(path), "MainWidget")
        widget: QPSLWidget = _class(None,
                                    virtual_mode=bool(self.m_virtual_mode))
        self.resize(widget.size())
        self.setCentralWidget(widget)

    def closeEvent(self, event: QCloseEvent):
        if self.m_is_single_plugin:
            if self.centralWidget() is not None:
                self.centralWidget().to_delete()
        self.showMinimized()
        for tab in self.m_tabs:
            tab.widget.to_delete()
            tab.set_widget(widget=None)
        configer_write()
        return super().closeEvent(event)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        if not self.m_is_single_plugin:
            if self.m_active_menudock:
                self.update_menudock_size()
        return super().resizeEvent(a0)

    def moveEvent(self, a0: QMoveEvent) -> None:
        if not self.m_is_single_plugin:
            if self.m_active_menudock:
                self.update_menudock_position()
        return super().moveEvent(a0)

    @property
    def python_plugins(self) -> QPSLMenuDock:
        return self.m_menudocks["python plugins"]

    # @property
    # def external_plugins(self) -> QPSLMenuDock:
    #     return self.m_menudocks["external plugins"]

    # @property
    # def combined_plugins(self) -> QPSLMenuDock:
    #     return self.m_menudocks["combined plugins"]
