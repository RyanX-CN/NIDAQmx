from Tool import *

os_path_append("./Plugins/NIDAQDOPlugin/bin")
from Plugins.NIDAQDOPlugin.NIDAQDOAPI import *
from PyQt5.QtCore import pyqtSignal

class NIDAQDOPluginWorker(QPSLWorker):
    signal_answer_device_list = pyqtSignal(list)
    signal_terminal_list = pyqtSignal(list)
    sig_answer_line_list = pyqtSignal(list)
    sig_task_inited = pyqtSignal()
    sig_task_cleared = pyqtSignal()
    sig_task_startted = pyqtSignal()
    sig_task_stopped = pyqtSignal()
    sig_write_data = pyqtSignal(int, np.ndarray)

    def __init__(self, parent: QWidget, object_name: str, virtual_mode: bool):
        super(NIDAQDOPluginWorker, self).__init__(parent=parent,
                                                object_name=object_name)
        self.m_task = DAQmxDigitalOutputTask()


class NIDAQDOPluginUI(QPSLTabWidget):
    
    def __init__(self,
                 parent: QWidget,
                 object_name="NIDAQDO",
                 virtual_mode=False,
                 font_family="Arial"):
        super(NIDAQDOPluginUI,self).__init__(parent=parent,
                                             object_name=object_name)
        self.m_font_family = font_family
        self.m_worker = NIDAQDOPluginWorker(self,
                                            object_name="worker",
                                            virtual_mode=virtual_mode)
        self.setupUi()
        self.setupStyle()
        self.setupLogic()
        self.on_nidaq_task_state_changed(False)
        self.m_worker.start_thread()
        self.init()

    @QPSLObjectBase.log_decorator()
    def setupUi(self):
        pass

    @QPSLObjectBase.log_decorator()
    def setupStyle(self):
        pass

    @QPSLObjectBase.log_decorator()
    def setupLogic(self):
        pass
    
MainWidget = NIDAQDOPluginUI

