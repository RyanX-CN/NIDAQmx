# @Last Modified by:  oldyan
# @Last Modified time: 2023-04-01 00:44:13

from QPSLClass.Base import *
from QPSLClass.QPSLDockWidget import QPSLDockWidget
from QPSLClass.QPSLMainWindow import QPSLMainWindow
from QPSLClass.QPSLMenuBar import QPSLMenuBar
from QPSLClass.QPSLMenuDock import QPSLMenuDock
from QPSLClass.QPSLPushButton import QPSLPushButton
from QPSLClass.QPSLScrollList import QPSLHScrollList
from QPSLClass.QPSLWidget import QPSLWidget


class QPSLStartMode_Normal(QPSLMainWindow):

    def __init__(self, object_name="window", window_title="QPSL-NIDAQMX"):
        super().__init__(parent=None, object_name=object_name)
        self.m_active_menudock = None
        self.setWindowTitle(window_title)
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

    def update_menudock_size(self):
        self.m_active_menudock: QPSLMenuDock
        self.m_active_menudock.resize(self.width(),
                                      self.m_active_menudock.height())

    def update_menudock_position(self):
        self.m_active_menudock: QPSLMenuDock
        self.m_active_menudock.move(
            self.menu_bar.mapToGlobal(self.menu_bar.rect().bottomLeft()))

    def closeEvent(self, event: QCloseEvent):
        self.showMinimized()
        for tab in self.m_tabs:
            tab.widget.to_delete()
            tab.set_widget(widget=None)
        return super().closeEvent(event)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        if self.m_active_menudock:
            self.update_menudock_size()
        return super().resizeEvent(a0)

    def moveEvent(self, a0: QMoveEvent) -> None:
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


class QPSLStartMode_AGADP(QPSLMainWindow):

    def __init__(
            self,
            object_name="window",
            window_title="AI-based Glaucoma Auxiliary Diagnosis Platform"):
        super().__init__(parent=None, object_name=object_name)
        from AGADP.AGADPMainPlugin.AGADPMainPlugin import AGADPMainPluginUI
        if self.login():
            self.setWindowTitle(window_title)
            self.resize(1320, 800)
            self.setCentralWidget(
                AGADPMainPluginUI(self,
                                  object_name="AGADP",
                                  font_family="Arial"))
        else:
            QTimer.singleShot(0, self.close)

    @property
    def centralWidget(self) -> QPSLWidget:
        return QMainWindow.centralWidget(self)

    def login(self):
        from AGADP.AGADPLoginPlugin.AGADPLoginPlugin import AGADPLoginPluginUI
        dialog = AGADPLoginPluginUI(None,
                                    object_name="login",
                                    window_title="AGADP login",
                                    init_username="admin",
                                    init_password="admin",
                                    log_in_keys={"admin": "admin"},
                                    font_family="Arial")
        dialog.resize(1200, 600)
        return dialog.exec()

    def closeEvent(self, event: QCloseEvent):
        if self.centralWidget is not None:
            self.centralWidget.to_delete()
        return super().closeEvent(event)
