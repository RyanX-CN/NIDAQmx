from QPSLClass.Base import *
from QPSLClass.QPSLAction import QPSLAction
from QPSLClass.QPSLActionGroup import QPSLActionGroup
from QPSLClass.QPSLBool import QPSLBool
from QPSLClass.QPSLDockWidget import QPSLDockWidget
from QPSLClass.QPSLMenu import QPSLMenu
from QPSLClass.QPSLMenuBar import QPSLMenuBar
from QPSLClass.QPSLMenuDock import QPSLMenuDock
from QPSLClass.QPSLWidget import QPSLWidget
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLMainWindow(QMainWindow, QPSLWidgetBase):
    sig_dockwidget_closed = pyqtSignal([], [QDockWidget])

    def __init__(self, parent: QWidget, object_name="window"):
        super(QPSLMainWindow, self).__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.m_tabs: List[QPSLDockWidget] = []
        self.m_actions: Dict[str, QAction] = dict()
        self.m_menudocks: Dict[str, QPSLMenuDock] = dict()
        self.m_virtual_mode = QPSLBool(False)
        connect_direct(self.sig_dockwidget_closed[QDockWidget],
                       self.remove_dockwidget)
        QPSLWidgetBase.add_global_style_controller()
        QPSLWidgetBase.set_global_app_style("Fusion")
        QPSLWidgetBase.add_global_console_log_level_controller()
        QPSLWidgetBase.set_global_console_log_level(level="INF")
        if "qdarkstyle" in sys.modules:
            QPSLWidgetBase.add_global_light_dark_style_controller()
        if "qt_material" in sys.modules:
            QPSLWidgetBase.add_global_material_themes_choices()
        QPSLWidgetBase.add_global_colored_log_switch()
        QPSLWidgetBase.set_global_colored_log_state(state=True)

    def add_dockwidget(self, widget: QPSLWidget) -> QPSLDockWidget:
        id = 0
        while any(w.windowTitle() == "%s_%d" % (widget.__class__.__name__, id)
                  for w in self.m_tabs):
            id += 1
        dock_widget = QPSLDockWidget(self,
                                     object_name="%s_%d" %
                                     (widget.__class__.__name__, id))
        dock_widget.set_widget(widget=widget)
        widget.set_QPSL_parent(qpsl_parent=dock_widget)
        dock_widget.setWindowTitle("{0}_{1}".format(widget.__class__.__name__,
                                                    id))
        if self.m_tabs:
            self.tabifyDockWidget(self.m_tabs[0], dock_widget)
        else:
            self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea,
                               dock_widget)
        self.m_tabs.append(dock_widget)
        return dock_widget

    def remove_dockwidget(self, dock_widget: QDockWidget):
        self.m_tabs.remove(dock_widget)
        dock_widget.deleteLater()

    def add_context_action_menu(self):
        if self.m_actions:
            self.menu_bar.add_separator()
        action = self.add_action(action_name="settings")
        menu = QPSLMenu(self.menu_bar, object_name="settings", title="")
        for act in QPSLWidgetBase.global_context_actions():
            if isinstance(act, QPSLAction):
                menu.addAction(act)
            elif isinstance(act, QPSLActionGroup):
                menu.addSection(act.objectName())
                menu.addActions(act.actions())
            else:
                menu.addSeparator()
        action.setMenu(menu)

    def add_action(self, action_name: str) -> QPSLAction:
        if self.m_actions:
            self.menu_bar.add_separator()
        self.m_actions[action_name] = QPSLAction(self.menu_bar,
                                                 object_name=action_name,
                                                 text=action_name,
                                                 checkable=False)
        self.menu_bar.addAction(self.m_actions[action_name])
        return self.m_actions[action_name]

    def add_virtual_mode_choice(self):
        action = QPSLAction(self.settings_menu,
                            object_name="virtual mode",
                            text="virtual mode",
                            checkable=True)
        self.settings_menu.addAction(action)
        connect_direct(action.triggered, self.m_virtual_mode.set_value)
        connect_direct(self.m_virtual_mode.sig_value_changed,
                       action.setChecked)

    def set_virtual_mode(self, state: bool):
        self.m_virtual_mode.set_value(val=state)

    @property
    def menu_bar(self) -> QPSLMenuBar:
        return super().menuBar()

    @property
    def settings_menu(self) -> QPSLMenu:
        return self.m_actions["settings"].menu()

    @property
    def action_virtual_mode(self) -> QPSLAction:
        return self.settings_menu.findChild(QPSLAction, "virtual mode")