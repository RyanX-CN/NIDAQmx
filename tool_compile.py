from Tool import *


class Compile_MainWindow(QPSLMainWindow):

    def __init__(self) -> None:
        """本界面窗口用于编译 C 语言/C++ 库
        """
        super().__init__(None)
        self.setWindowTitle("compile")
        self.m_widget = QPSLVerticalGroupList(self, "widget")

        self.m_btn_bin = QPSLChooseDirButton(self.m_widget,
                                             object_name="btn_bin",
                                             prefix="bin:")
        self.m_btn_bin.set_tooltip_enable()
        self.m_btn_include_path = QPSLChooseDirButton(
            self.m_widget, object_name="btn_include", prefix="include:")
        self.m_btn_include_path.set_tooltip_enable()
        self.m_btn_lib_path = QPSLChooseDirButton(self.m_widget,
                                                  object_name="btn_lib",
                                                  prefix="lib:")
        self.m_btn_lib_path.set_tooltip_enable()
        self.m_btn_libs = QPSLChooseOpenFilesButton(self.m_widget,
                                                    object_name="btn_libs",
                                                    prefix="libs:")
        self.m_btn_libs.set_tooltip_enable()
        self.m_btn_source_path = QPSLChooseOpenFileButton(
            self.m_widget, object_name="btn_source", prefix="source:")
        self.m_btn_source_path.set_tooltip_enable()
        self.m_edit_dll_fname = QPSLTextLineEdit(self.m_widget,
                                                 object_name="edit_dll_fname",
                                                 key_text="dll_file_name:")
        self.m_edit_args = QPSLTextLineEdit(self.m_widget,
                                            object_name="edit_args",
                                            key_text="args:")
        self.m_edit_args.set_text(text="-O3")
        self.m_label = QPSLLabel(self.m_widget,
                                 object_name="label",
                                 text="right click to auto fill")
        self.m_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.m_btn_make_command = QPSLPushButton(
            self.m_widget, object_name="btn_make_command", text="make command")
        self.m_btn_gcc_compile = QPSLPushButton(self.m_widget,
                                                object_name="btn_compile",
                                                text="compile")
        self.m_btn_try_load_dll = QPSLPushButton(
            self.m_widget, object_name="btn_try_load_dll", text="try load dll")

        def callback(fname: str):
            fname = get_pure_filename(fname)
            self.m_edit_dll_fname.set_text(
                text="{0}.dll".format(fname[:fname.rfind('.')]))

        connect_direct(self.m_btn_source_path.sig_choose_path[str], callback)
        connect_direct(self.m_btn_make_command.sig_clicked, self.make_command)
        connect_direct(self.m_btn_gcc_compile.sig_clicked, self.gcc_compile)
        connect_direct(self.m_btn_try_load_dll.sig_clicked, self.try_load_dll)

        self.m_widget.add_widgets(widgets=[
            self.m_btn_bin, self.m_btn_include_path, self.m_btn_lib_path,
            self.m_btn_libs, self.m_btn_source_path, self.m_edit_dll_fname,
            self.m_edit_args, self.m_label, self.m_btn_make_command,
            self.m_btn_gcc_compile, self.m_btn_try_load_dll
        ])
        self.m_widget.set_stretch(sizes=(1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2))
        self.setCentralWidget(self.m_widget)
        self.resize(500, 500)

        dic: Dict[str, List[str]] = {
            "Plugins": ["DMPlugin", "NIDAQAIPlugin", "NIDAQAOPlugin"]
        }
        self.m_label.add_separator()
        for menu_name, plugin_names in dic.items():
            for plugin_name in plugin_names:
                act = self.m_label.add_context_action(
                    action_name="{0}.{1}".format(menu_name, plugin_name))

                def wrap(menu_name, plugin_name):

                    def inner():
                        self.auto_fill(menu_path=os.path.abspath(menu_name),
                                       plugin_name=plugin_name)

                    return inner

                connect_direct(
                    act.triggered,
                    wrap(menu_name=menu_name, plugin_name=plugin_name))

    def auto_fill(self, menu_path: str, plugin_name: str):
        path = os.path.abspath(os.path.join(menu_path, plugin_name))
        if os.path.exists(os.path.join(path, "bin")):
            self.m_btn_bin.choose_path(
                path=os.path.abspath(os.path.join(path, "bin")))
        if os.path.exists(os.path.join(path, "include")):
            self.m_btn_include_path.choose_path(
                path=os.path.abspath(os.path.join(path, "include")))
        if os.path.exists(os.path.join(path, "lib")):
            self.m_btn_lib_path.choose_path(
                path=os.path.abspath(os.path.join(path, "lib")))
            paths = list(
                listdir(dir_path=os.path.abspath(os.path.join(path, "lib"))))
            self.m_btn_libs.choose_paths(paths=paths)
        if os.path.exists(os.path.join(path, "source")) and any(
                listdir(os.path.join(path, "source"))):
            fname = next(listdir(os.path.join(path, "source")))
            self.m_btn_source_path.choose_path(path=os.path.abspath(fname))

    def make_command(self):
        para = ["-shared", "-fPIC"]
        if self.m_btn_include_path.get_path():
            para.append("-I{0}".format(self.m_btn_include_path.get_path()))
        if self.m_btn_lib_path.get_path():
            para.append("-L{0}".format(self.m_btn_lib_path.get_path()))
        if self.m_btn_libs.get_paths():
            for lib in self.m_btn_libs.get_paths():
                para.append("-l{0}".format('.'.join(
                    get_pure_filename(lib).split('.')[:-1])))
        source_file = self.m_btn_source_path.get_path()
        dll_file = os.path.join(self.m_btn_bin.get_path(),
                                self.m_edit_dll_fname.text())
        if self.m_edit_args.text():
            para.append(self.m_edit_args.text())
        self.m_command = "g++ {0} -o {1} {2}".format(source_file, dll_file,
                                                     ' '.join(para))
        message_box = QPSLMessageBox(None,
                                     object_name="box_message",
                                     window_title="command",
                                     text=self.m_command)
        message_box.exec()

    def gcc_compile(self):
        if not self.m_command:
            return
        res = os.system(self.m_command)
        loading_info("compile res = {0}".format(res))

    def try_load_dll(self):
        os_path_append(self.m_btn_bin.get_path())
        try:
            dll = load_dll(dll_file_path=self.m_edit_dll_fname.text())
        except BaseException as e:
            loading_error("failed to load dll, error = {0}".format(e))
        else:
            loading_info("made it to load dll, {0}".format(dll))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Compile_MainWindow()
    main_window.show()
    sys.exit(app.exec_())
