from QPSLClass.Base import *
from QPSLClass.QPSLAction import QPSLAction
from QPSLClass.QPSLActionGroup import QPSLActionGroup
from QPSLClass.QPSLLayout import QPSLGridLayout
from QPSLClass.QPSLObjectBase import QPSLObjectBase


class QPSLWidgetBase(QPSLObjectBase):
    __context_actions: List[Union[QPSLAction, QPSLActionGroup]] = []
    __set_app_style_callback: List[Callable] = []
    __set_log_threshold_callback: List[Callable] = []
    __set_light_dark_style_callback: List[Callable] = []
    __set_color_state_callback: List[Callable] = []

    @classmethod
    def global_context_actions(cls):
        return cls.__context_actions

    @classmethod
    def global_style_callback(cls):
        return cls.__set_app_style_callback

    @classmethod
    def global_set_console_log_level_callback(cls):
        return cls.__set_log_threshold_callback

    @classmethod
    def global_light_dark_callback(cls):
        return cls.__set_light_dark_style_callback

    @classmethod
    def add_global_separator(cls):
        cls.global_context_actions().append(...)

    @classmethod
    def add_global_context_action(cls, action_name: str):
        act = QPSLAction(None,
                         object_name=action_name,
                         text=action_name,
                         checkable=False)
        cls.global_context_actions().append(act)
        return act

    @classmethod
    def add_global_context_actions_switch(
            cls, action_name: str,
            trigger_callback: Callable) -> Callable[..., None]:
        action = QPSLAction(None,
                            object_name=action_name,
                            text=action_name,
                            checkable=True)
        cls.global_context_actions().append(action)
        connect_direct(action.triggered, trigger_callback)
        return action.setChecked

    @classmethod
    def add_global_context_actions_single_choice(
            cls, action_name_list: Iterable[str], group_name: str,
            trigger_callback: Callable) -> Callable[..., None]:
        action_group = QPSLActionGroup(None, object_name=group_name)
        for action_name in action_name_list:
            action_group.addAction(
                QPSLAction(action_group,
                           object_name=action_name,
                           text=action_name,
                           checkable=True))
        cls.global_context_actions().append(action_group)

        def trigger_wrap(action: QPSLAction):
            trigger_callback(action.objectName())

        connect_direct(action_group.triggered, trigger_wrap)

        def set_trigger(action_name):
            action_group.findChild(QPSLAction, action_name).setChecked(True)

        return set_trigger

    @classmethod
    def add_global_context_actions_list(cls, action_name: str,
                                        items: List[str], callback):
        act = QPSLAction(None,
                         object_name=action_name,
                         text=action_name,
                         checkable=False)
        cls.global_context_actions().append(act)

        def show_list():

            dialog = QDialog(None)
            dialog.setWindowTitle(action_name)
            dialog.setLayout(QPSLGridLayout(dialog))
            a_list = QListWidget(dialog)
            a_list.addItems(items)

            def double_click_callback():
                callback(a_list.currentItem().text())

            connect_direct(a_list.itemDoubleClicked, double_click_callback)

            dialog.layout().addWidget(a_list)
            dialog.exec()

        connect_direct(act.triggered, show_list)

    @classmethod
    def add_global_style_controller(cls):
        set_style_trigger = cls.add_global_context_actions_single_choice(
            action_name_list=QStyleFactory.keys(),
            group_name="style_control",
            trigger_callback=cls.set_global_app_style)
        cls.global_style_callback().append(set_style_trigger)

    @staticmethod
    def set_global_app_style(style: str):
        QApplication.setStyle(QStyleFactory.create(style))
        for f in QPSLWidgetBase.global_style_callback():
            f(style)

    @classmethod
    def add_global_console_log_level_controller(cls):
        set_log_threshold_trigger = cls.add_global_context_actions_single_choice(
            action_name_list=QPSL_LOG_LEVEL._member_names_,
            group_name="log_threshold",
            trigger_callback=cls.set_global_console_log_level)
        cls.global_set_console_log_level_callback().append(
            set_log_threshold_trigger)

    @classmethod
    def set_global_console_log_level(cls, level: str):
        set_console_log_level(level=QPSL_LOG_LEVEL._member_map_[level])
        for f in cls.global_set_console_log_level_callback():
            f(level)

    @classmethod
    def add_global_material_themes_choices(cls):
        cls.add_global_separator()
        cls.add_global_context_actions_list(action_name="themes...",
                                            items=qt_material.list_themes(),
                                            callback=cls.set_global_app_theme)

    @staticmethod
    def set_global_app_theme(theme: str):
        qt_material.apply_stylesheet(QApplication.instance(), theme=theme)

    @classmethod
    def add_global_light_dark_style_controller(cls):
        set_light_dark_style_trigger = cls.add_global_context_actions_single_choice(
            action_name_list=("light", "dark"),
            group_name="dark/light style",
            trigger_callback=cls.set_global_light_dark_style)
        cls.global_light_dark_callback().append(set_light_dark_style_trigger)

    @staticmethod
    def set_global_light_style():
        QApplication.instance().setStyleSheet(
            qdarkstyle.load_stylesheet(qt_api='pyqt5',
                                       palette=qdarkstyle.LightPalette))

    @staticmethod
    def set_global_dark_style():
        QApplication.instance().setStyleSheet(
            qdarkstyle.load_stylesheet(qt_api='pyqt5',
                                       palette=qdarkstyle.DarkPalette))

    @staticmethod
    def set_global_light_dark_style(style: str):
        if style == "light":
            QPSLWidgetBase.set_global_light_style()
        elif style == "dark":
            QPSLWidgetBase.set_global_dark_style()
        for f in QPSLWidgetBase.global_light_dark_callback():
            f(style)

    @classmethod
    def add_global_colored_log_switch(cls):
        cls.__set_color_state_callback.append(
            cls.add_global_context_actions_switch(
                action_name="colored log",
                trigger_callback=cls.set_global_colored_log_state))

    @classmethod
    def set_global_colored_log_state(cls, state: bool):
        ColoredConsoleHandler.color_state = state
        for f in cls.__set_color_state_callback:
            f(state)

    def __init__(self):
        super().__init__()
        self.m_tooltip_enable = False
        self.m_context_actions: List[Union[QPSLAction, QPSLActionGroup]] = []
        QWidget.setSizePolicy(self, QSizePolicy.Policy.Preferred,
                              QSizePolicy.Policy.Preferred)
        self.set_custom_context_menu()
        self.add_separator()
        self.add_context_action_font_choices()
        self.add_context_action_background_color_choices()
        self.add_context_action_foregound_color_choices()

    def set_tooltip_enable(self):
        if not self.m_tooltip_enable:
            self.m_tooltip_enable = True

    def set_tooltip_disable(self):
        if self.m_tooltip_enable:
            self.m_tooltip_enable = False

    def set_custom_context_menu(self):
        QWidget.setContextMenuPolicy(self,
                                     Qt.ContextMenuPolicy.CustomContextMenu)
        connect_direct(getattr(self, "customContextMenuRequested"),
                       self.show_custom_context_menu)

    def unset_custom_context_menu(self):
        disconnect(getattr(self, "customContextMenuRequested"),
                   self.show_custom_context_menu)

    def update_palette(self, role: QPalette.ColorRole,
                       color: typing.Union[str, QColor, Qt.GlobalColor]):
        if isinstance(color, str):
            color = QColor(color)
        palette = QWidget.palette(self)
        palette.setColor(role, color)
        QWidget.setPalette(self, palette)

    def get_background_color_role(self):
        if isinstance(self, QPushButton):
            return QPalette.ColorRole.Button
        else:
            return QPalette.ColorRole.Window

    def get_foreground_color_role(self):
        if isinstance(self, QPushButton):
            return QPalette.ColorRole.ButtonText
        else:
            return QPalette.ColorRole.WindowText

    def update_window_palette(self, color: typing.Union[str, QColor,
                                                        Qt.GlobalColor]):
        if isinstance(color, str):
            color = QColor(color)
        QWidget.setAutoFillBackground(self, True)
        palette = QWidget.palette(self)
        palette.setColor(QPalette.ColorRole.Window, color)
        QWidget.setPalette(self, palette)

    def update_button_palette(self, color: typing.Union[str, QColor,
                                                        Qt.GlobalColor]):
        if isinstance(color, str):
            color = QColor(color)
        QWidget.setAutoFillBackground(self, True)
        palette = QWidget.palette(self)
        palette.setColor(QPalette.ColorRole.Button, color)
        QWidget.setPalette(self, palette)

    def update_background_palette(self, color: typing.Union[str, QColor,
                                                            Qt.GlobalColor]):
        if isinstance(color, str):
            color = QColor(color)
        QWidget.setAutoFillBackground(self, True)
        palette = QWidget.palette(self)
        palette.setColor(self.get_background_color_role(), color)
        QWidget.setPalette(self, palette)

    def update_windowtext_palette(self, color: typing.Union[str, QColor,
                                                            Qt.GlobalColor]):
        if isinstance(color, str):
            color = QColor(color)
        QWidget.setAutoFillBackground(self, True)
        palette = QWidget.palette(self)
        palette.setColor(QPalette.Foreground, color)
        QWidget.setPalette(self, palette)

    def update_buttontext_palette(self, color: typing.Union[str, QColor,
                                                            Qt.GlobalColor]):
        if isinstance(color, str):
            color = QColor(color)
        QWidget.setAutoFillBackground(self, True)
        palette = QWidget.palette(self)
        palette.setColor(QPalette.ButtonText, color)
        QWidget.setPalette(self, palette)

    def update_foreground_palette(self, color: typing.Union[str, QColor,
                                                            Qt.GlobalColor]):
        if isinstance(color, str):
            color = QColor(color)
        QWidget.setAutoFillBackground(self, True)
        palette = QWidget.palette(self)
        palette.setColor(self.get_foreground_color_role(), color)
        QWidget.setPalette(self, palette)

    def add_separator(self):
        self.m_context_actions.append(...)

    def add_context_action(self, action_name: str):
        self.m_context_actions.append(
            QPSLAction(self,
                       object_name=action_name,
                       text=action_name,
                       checkable=False))
        return self.m_context_actions[-1]

    def add_context_actions_single_choice(
            self, action_name_list: List[str], group_name: str,
            callback: Callable) -> Callable[..., None]:
        action_group = QPSLActionGroup(self, object_name=group_name)
        for action_name in action_name_list:
            action_group.addAction(
                QPSLAction(action_group,
                           object_name=action_name,
                           text=action_name,
                           checkable=True))
        self.m_context_actions.append(action_group)

        def inner(action: QPSLAction):
            callback(action.text())

        connect_direct(action_group.triggered, inner)

        def set_trigger(action_name):
            action_group.findChild(QPSLAction, action_name).setChecked(True)

        return set_trigger

    def add_context_actions_list(self, action_name: str, items: List[str],
                                 callback):
        act = QPSLAction(self,
                         object_name=action_name,
                         text=action_name,
                         checkable=False)
        self.m_context_actions.append(act)

        def show_list():

            dialog = QDialog(None)
            dialog.setWindowTitle(action_name)
            dialog.setLayout(QPSLGridLayout(dialog))
            a_list = QListWidget(dialog)
            a_list.addItems(items)

            def double_click_callback():
                callback(a_list.currentItem().text())

            connect_direct(a_list.itemDoubleClicked, double_click_callback)

            dialog.layout().addWidget(a_list)
            dialog.exec()

        connect_direct(act.triggered, show_list)

    def add_context_action_font_choices(self):
        act = QPSLAction(self,
                         object_name="act_font",
                         text="font...",
                         checkable=False)
        self.m_context_actions.append(act)

        def callback():
            old_font = QWidget.font(self)
            dialog = QFontDialog(old_font, None)

            def select_font(font: QFont):
                QWidget.setFont(self, font)

            connect_direct(dialog.currentFontChanged, select_font)
            if dialog.exec() != QDialog.Accepted:
                QWidget.setFont(self, old_font)

        connect_direct(act.triggered, callback)

    def add_context_action_background_color_choices(self):
        act = QPSLAction(self,
                         object_name="act_background_color",
                         text="background color...",
                         checkable=False)
        self.m_context_actions.append(act)

        def callback():
            old_palette = QWidget.palette(self)
            dialog = QColorDialog(
                old_palette.color(self.get_background_color_role()), None)
            autofill = QWidget.autoFillBackground(self)
            QWidget.setAutoFillBackground(self, True)

            connect_direct(dialog.currentColorChanged,
                           self.update_background_palette)
            if dialog.exec() != QDialog.Accepted:
                QWidget.setAutoFillBackground(self, autofill)
                QWidget.setPalette(self, old_palette)

        connect_direct(act.triggered, callback)

    def add_context_action_foregound_color_choices(self):
        act = QPSLAction(self,
                         object_name="act_foreground_color",
                         text="foreground color...",
                         checkable=False)
        self.m_context_actions.append(act)

        def callback():
            old_palette = QWidget.palette(self)
            dialog = QColorDialog(
                old_palette.color(self.get_foreground_color_role()), None)
            autofill = QWidget.autoFillBackground(self)
            QWidget.setAutoFillBackground(self, True)

            connect_direct(dialog.currentColorChanged,
                           self.update_foreground_palette)
            if dialog.exec() != QDialog.Accepted:
                QWidget.setAutoFillBackground(self, autofill)
                QWidget.setPalette(self, old_palette)

        connect_direct(act.triggered, callback)

    def show_attribute_dialog(self):
        dialog = QDialog(None)
        dialog.setWindowTitle("attribute")
        dialog.setLayout(QPSLGridLayout(dialog))
        edit = QLineEdit(dialog)
        dialog.layout().addWidget(edit)

        def callback():
            try:
                exec(edit.text(), {'self': self})
            except BaseException as e:
                self.add_error(msg=e)

        connect_direct(edit.returnPressed, callback)
        dialog.exec()

    def show_custom_context_menu(self, pos: QPoint):
        menu = QMenu(self)

        @weakref_local_function(self)
        def clipboard_set_trace_path(self: QPSLObjectBase):
            clipboard_setText(self.trace_path())

        def short_str(name: str):
            if len(name) <= 30:
                return name
            else:
                return "...{0}".format(name[-27:])

        menu.addAction(short_str(self.trace_path()), clipboard_set_trace_path)
        for act in self.global_context_actions() + self.m_context_actions:
            if isinstance(act, QPSLAction):
                menu.addAction(act)
            elif isinstance(act, QPSLActionGroup):
                menu.addSection(act.objectName())
                menu.addActions(act.actions())
            else:
                menu.addSeparator()
        menu.addSeparator()
        menu.addAction("attrs.", self.show_attribute_dialog)
        menu.exec(QWidget.mapToGlobal(self, pos))
