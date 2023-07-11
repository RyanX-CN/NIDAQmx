from QPSLClass.Base import *
from QPSLClass.QPSLGroupList import QPSLHorizontalGroupList, QPSLVerticalGroupList
from QPSLClass.QPSLPushButton import QPSLPushButton
from QPSLClass.QPSLSpinBox import QPSLSpinBox
from QPSLClass.QPSLPlot import QPSLPlot


class QPSLRotatePlot(QPSLHorizontalGroupList):
    sig_work_started = pyqtSignal()
    sig_work_stopped = pyqtSignal()
    sig_to_handle = pyqtSignal()

    def __init__(self, parent: QWidget, object_name: str):
        super().__init__(parent=parent, object_name=object_name)
        self.add_widget(widget=QPSLPlot(self, object_name="plot"))
        self.add_widget(widget=QPSLVerticalGroupList(self, object_name="control"))
        self.control.add_widget(widget=QPSLSpinBox(self.control,
                                                   object_name="spin_plot",
                                                   min=1,
                                                   max=10000,
                                                   value=15,
                                                   prefix="plot:"))
        self.control.add_widget(widget=QPSLSpinBox(self.control,
                                                   object_name="spin_ds",
                                                   min=1,
                                                   max=10000,
                                                   value=1,
                                                   prefix="ds:"))
        self.control.add_widget(widget=QPSLPushButton(
            self.control, object_name="btn_clear", text="clear"))
        connect_direct(self.spin_plot.sig_editing_finished[int], self.prepare)
        connect_direct(self.spin_ds.sig_editing_finished[int],
                       self.plot.set_downsample)
        connect_direct(self.btn_clear.sig_clicked, self.clear_plots)
        self.m_plots = deque()
        self.m_data = deque()
        self.m_data_mut = QMutex()
        self.m_keep_query = SharedStateController(
            value=SharedStateController.State.Stop)
        connect_queued(self.sig_to_handle, self.handle)
        self.control.hide()
    @property
    def plot(self) -> QPSLPlot:
        return self.get_widget(0)

    @property
    def control(self) -> QPSLVerticalGroupList:
        return self.get_widget(1)

    @property
    def spin_plot(self) -> QPSLSpinBox:
        return self.control.get_widget(0)

    @property
    def spin_ds(self) -> QPSLSpinBox:
        return self.control.get_widget(1)

    @property
    def btn_clear(self) -> QPSLPushButton:
        return self.control.get_widget(2)

    def prepare(self, n: int):
        self.m_plot_n = n

    def add_data(self, x: np.ndarray, y: np.ndarray):
        self.m_data_mut.lock()
        self.m_data.append((x, y))
        self.m_data_mut.unlock()

    def handle(self):
        self.m_data_mut.lock()
        while self.m_data:
            x, y = self.m_data.popleft()
            if self.m_plot_n < len(self.m_plots):
                plot = self.m_plots.popleft()
                self.plot.remove_item(item=plot)
                plot = self.m_plots.popleft()
            elif self.m_plot_n > len(self.m_plots):
                plot = self.plot.add_item()
            else:
                plot = self.m_plots.popleft()
            plot.setData(x=x, y=y)
            self.m_plots.append(plot)
        self.m_data_mut.unlock()
        self.plot.re_plot()

    def clear_plots(self):
        for plot in self.m_plots:
            plot.setData(x=None, y=None)
        self.plot.re_plot()

    def start_work(self):
        self.prepare(n=self.spin_plot.value())
        self.plot.set_downsample(ds=self.spin_ds.value())
        if self.m_keep_query.is_continue():
            return

        def func():
            while not self.m_keep_query.reply_if_stop():
                self.sig_to_handle.emit()
                sleep_for(20)

        self.m_keep_query.set_continue()
        QThreadPool.globalInstance().start(func)
        self.sig_work_started.emit()

    def stop_work(self):
        if self.m_keep_query.is_stop():
            return
        self.m_keep_query.set_stop_until_reply()
        self.sig_work_stopped.emit()