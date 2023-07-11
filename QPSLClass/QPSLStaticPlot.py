from QPSLClass.Base import *
from QPSLClass.QPSLGroupList import QPSLHorizontalGroupList, QPSLVerticalGroupList
from QPSLClass.QPSLPushButton import QPSLPushButton
from QPSLClass.QPSLSpinBox import QPSLSpinBox
from QPSLClass.QPSLPlot import QPSLPlot


class QPSLStaticPlot(QPSLPlot):
    sig_work_started = pyqtSignal()
    sig_work_stopped = pyqtSignal()
    sig_to_handle = pyqtSignal()

    def __init__(self, parent: QWidget, object_name: str):
        super().__init__(parent=parent, object_name=object_name)
        self.m_plot = self.add_item()

    def set_data(self, arr: np.ndarray):
        self.m_plot.setData(arr)
        self.re_plot()

    # def clear(self):
    #     for plot in self.m_plots:
    #         plot.setData(x=None, y=None)
    #     self.plot.re_plot()
