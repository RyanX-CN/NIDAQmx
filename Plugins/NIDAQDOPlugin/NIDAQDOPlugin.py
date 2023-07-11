from Tool import *

os_path_append("./Plugins/NIDAQDOPlugin/bin")
from Plugins.NIDAQDOPlugin.NIDAQDOAPI import *

class NIDAQDOPluginWorker(QPSLWorker):
    pass

class NIDAQDOPluginUI(QPSLTabWidget):
    pass

MainWidget = NIDAQDOPluginUI

