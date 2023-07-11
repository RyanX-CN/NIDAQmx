from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLPushButton(QPushButton, QPSLWidgetBase):
    sig_clicked = pyqtSignal([], [QPushButton], [str])

    def __init__(self, parent: QWidget, object_name: str, text: str = "press"):
        super().__init__(parent=parent)
        self.m_text = text
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.set_text(text=text)
        self.setSizePolicy(QSizePolicy.Policy.Ignored,
                           QSizePolicy.Policy.Ignored)
        connect_direct(self.clicked, self.on_clicked)

    def set_tooltip_enable(self):
        super().set_tooltip_enable()
        self.update_tooltip()

    def set_tooltip_disable(self):
        super().set_tooltip_disable()
        self.update_tooltip()

    def set_text(self, text: str):
        self.m_text = text
        self.update_text(text)
        self.update_tooltip()

    def set_font(self, font: QFont):
        super().setFont(font)
        self.update_text(text=self.m_text)

    def text(self):
        return self.m_text

    def update_text(self, text: str):
        w = self.fontMetrics().width(text)
        if w > self.width():
            self.setText(self.fontMetrics().elidedText(
                text, Qt.TextElideMode.ElideRight, self.width()))
        else:
            self.setText(text)

    def update_tooltip(self):
        if self.m_tooltip_enable:
            self.setToolTip(self.text())
        else:
            self.setToolTip("")

    def on_clicked(self, checked: bool):
        self.sig_clicked.emit()
        self.sig_clicked[QPushButton].emit(self)
        self.sig_clicked[str].emit(self.text())

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.update_text(self.m_text)
        return super().resizeEvent(a0)


class QPSLToggleButton(QPSLPushButton):
    sig_open = pyqtSignal()
    sig_close = pyqtSignal()
    sig_opened = pyqtSignal()
    sig_closed = pyqtSignal()
    sig_state_changed = pyqtSignal(bool)

    def __init__(
            self,
            parent: QWidget,
            object_name: str,
            closed_text="open",
            opened_text="close",
            closed_background_color: typing.Union[str, QColor,
                                                  Qt.GlobalColor] = "#a2a2a2",
            opened_background_color: typing.Union[str, QColor,
                                                  Qt.GlobalColor] = "#ffffff",
            state: bool = False):
        super().__init__(parent=parent, object_name=object_name)
        self.m_state = False
        self.m_closed_text = closed_text
        self.m_opened_text = opened_text
        self.m_closed_background_color = closed_background_color
        self.m_opened_background_color = opened_background_color
        self.set_state(opened=state)

    def get_state(self):
        return self.m_state

    def set_texts(self, closed_text: str, opened_text: str):
        self.m_closed_text = closed_text
        self.m_opened_text = opened_text
        self.set_state(opened=self.m_state)

    def set_background_colors(
            self, closed_background_color: typing.Union[str, QColor,
                                                        Qt.GlobalColor],
            opened_background_color: typing.Union[str, QColor,
                                                  Qt.GlobalColor]):
        self.m_closed_background_color = closed_background_color
        self.m_opened_background_color = opened_background_color
        self.set_state(opened=self.m_state)

    def set_state(self, opened: bool):
        self.m_state = opened
        if self.m_state:
            self.set_text(text=self.m_opened_text)
            if self.m_opened_background_color:
                self.update_background_palette(
                    color=self.m_opened_background_color)
            self.sig_opened.emit()
            self.sig_state_changed.emit(True)
        else:
            self.set_text(text=self.m_closed_text)
            if self.m_closed_background_color:
                self.update_background_palette(
                    color=self.m_closed_background_color)
            self.sig_closed.emit()
            self.sig_state_changed.emit(False)

    def set_opened(self):
        self.set_state(opened=True)

    def set_closed(self):
        self.set_state(opened=False)

    def on_clicked(self, checked: bool):
        if self.m_state:
            self.sig_close.emit()
        else:
            self.sig_open.emit()
        return super().on_clicked(checked)


class QPSLChoosePathButtonBase(QPSLPushButton):
    sig_choose_path = pyqtSignal([], [str])

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 prefix="path:",
                 init_path="",
                 filter: Union[str, Tuple[str]] = ""):
        super().__init__(parent=parent, object_name=object_name)
        self.set_prefix(prefix)
        self.set_path(path=init_path)
        self.set_filter(filter)

    def set_prefix(self, prefix: str):
        self.m_prefix = prefix

    def get_path(self):
        return self.m_path

    def set_path(self, path: str):
        self.m_path = path
        self.set_text(text=self.m_prefix + self.m_path)

    def set_filter(self, filter: Union[str, Tuple[str]]):
        self.m_filter = []
        if isinstance(filter, str):
            x = filter
            if x:
                self.m_filter.append(f"{x} files(*.{x})")
            else:
                self.m_filter.append(f"all files(*)")
        else:
            for x in filter:
                if x:
                    self.m_filter.append(f"{x} files(*.{x})")
                else:
                    self.m_filter.append(f"all files(*)")
        self.m_filter = ';;'.join(self.m_filter)

    def choose_path(self, path: str):
        if not path:
            return
        self.m_path = path
        self.set_text(text="%s%s" % (self.m_prefix, path))
        self.sig_choose_path.emit()
        self.sig_choose_path[str].emit(path)


class QPSLChooseSaveFileButton(QPSLChoosePathButtonBase):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 prefix="path:",
                 init_path="",
                 filter: Union[str, Tuple[str]] = ""):
        super().__init__(parent=parent,
                         object_name=object_name,
                         prefix=prefix,
                         init_path=init_path,
                         filter=filter)
        connect_direct(self.sig_clicked, self.on_click_and_choose)

    def on_click_and_choose(self):
        res = QFileDialog.getSaveFileName(parent=None,
                                          caption=self.m_prefix,
                                          directory=self.m_path,
                                          filter=self.m_filter)
        self.choose_path(path=res[0])


class QPSLChooseOpenFileButton(QPSLChoosePathButtonBase):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 prefix="path:",
                 init_path="",
                 filter: Union[str, Tuple[str]] = ""):
        super().__init__(parent=parent,
                         object_name=object_name,
                         prefix=prefix,
                         init_path=init_path,
                         filter=filter)
        connect_direct(self.sig_clicked, self.on_click_and_choose)

    def on_click_and_choose(self):
        res = QFileDialog.getOpenFileName(parent=None,
                                          caption=self.m_prefix,
                                          directory=self.m_path,
                                          filter=self.m_filter)
        self.choose_path(path=res[0])


class QPSLChooseDirButton(QPSLChoosePathButtonBase):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 prefix="path:",
                 init_path="",
                 filter: Union[str, Tuple[str]] = ""):
        super().__init__(parent=parent,
                         object_name=object_name,
                         prefix=prefix,
                         init_path=init_path,
                         filter=filter)
        connect_direct(self.sig_clicked, self.on_click_and_choose)

    def on_click_and_choose(self):
        res = QFileDialog.getExistingDirectory(parent=None,
                                               caption=self.m_prefix,
                                               directory=self.m_path)
        self.choose_path(path=res)


class QPSLChooseOpenFilesButton(QPSLChoosePathButtonBase):
    sig_choose_paths = pyqtSignal(list)

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 prefix="path:",
                 init_paths: Union[str, List[str]] = [],
                 filter: Union[str, Tuple[str]] = ""):
        if isinstance(init_paths, str):
            init_paths = init_paths.split(';')
        super().__init__(parent=parent,
                         object_name=object_name,
                         prefix=prefix,
                         init_path='',
                         filter=filter)
        self.set_paths(paths=init_paths)
        connect_direct(self.sig_clicked, self.on_click_and_choose)

    def get_paths(self):
        return self.m_paths

    def set_paths(self, paths: Union[str, List[str]]):
        if isinstance(paths, str):
            paths = paths.split(';')
        self.m_paths = paths
        self.set_text(text="{0}{1}".format(self.m_prefix, self.m_path))

    def on_click_and_choose(self):
        res = QFileDialog.getOpenFileNames(parent=None,
                                           caption=self.m_prefix,
                                           directory=self.m_path,
                                           filter=self.m_filter)
        self.choose_paths(res[0])

    def choose_paths(self, paths: Union[str, List[str]]):
        if isinstance(paths, str):
            paths = paths.split(';')
        if not paths:
            return
        self.m_paths = paths
        self.set_text(text="{0}{1}".format(self.m_prefix, ';'.join(paths)))
        self.sig_choose_path.emit()
        self.sig_choose_path[str].emit(';'.join(paths))
        self.sig_choose_paths[list].emit(paths)
