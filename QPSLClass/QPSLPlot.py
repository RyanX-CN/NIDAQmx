from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase


class QPSLPlot(pyqtgraph.PlotWidget, QPSLWidgetBase):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 background: str = 'default',
                 plotItem: Any = None,
                 **kargs):
        super().__init__(parent=parent,
                         background=background,
                         plotItem=plotItem,
                         kargs=kargs)
        self.set_QPSL_parent(qpsl_parent=parent)
        QObject.setObjectName(self, object_name)
        self.unset_custom_context_menu()
        self.getPlotItem().setClipToView(clip=True)

    def add_item(self):
        item = pyqtgraph.PlotDataItem()
        self.getPlotItem().addItem(item=item)
        return item

    def remove_item(self, item: pyqtgraph.PlotDataItem):
        self.getPlotItem().removeItem(item=item)

    def set_downsample(self, ds: int):
        self.getPlotItem().setDownsampling(ds=ds, auto=False, mode='subsample')

    def re_plot(self):
        self.getPlotItem().replot()


# class QPSLDotChartData(pyqtgraph.PlotDataItem, QPSLObjectBase):
#     def __init__(self, capacity):
#         super(QPSLDotChartData, self).__init__()
#         self.setDownsampling(ds=10, method='subsample')
#         self.set_capacity(capacity)
#         self.clear_data()

#     def set_capacity(self, capacity):
#         self.m_data_x = np.empty(shape=[capacity])
#         self.m_data_y = np.empty(shape=[capacity])
#         self.m_capacity = capacity

#     def add_data(self, data_x, data_y):
#         new_data_length = len(data_x)
#         if self.m_length+new_data_length <= self.m_capacity:
#             self.m_data_x[self.m_length:self.m_length+new_data_length] = data_x
#             self.m_data_y[self.m_length:self.m_length+new_data_length] = data_y
#         else:
#             self.m_data_x[:-new_data_length] = self.m_data_x[new_data_length:]
#             self.m_data_x[-new_data_length:] = data_x
#             self.m_data_y[:-new_data_length] = self.m_data_y[new_data_length:]
#             self.m_data_y[-new_data_length:] = data_y
#         self.m_length += new_data_length

#     def flush_data(self):
#         if self.m_length < self.m_capacity:
#             self.setData(x=self.m_data_x[:self.m_length],
#                          y=self.m_data_y[:self.m_length])
#         else:
#             self.setData(x=self.m_data_x, y=self.m_data_y)

#     def clear_data(self):
#         self.m_length = 0

# class QPSLPlot(pyqtgraph.PlotWidget, QPSLWidgetBase):
#     def __init__(self, parent):
#         super(QPSLPlot, self).__init__(parent=parent)

#     def add_dot_chart(self, capacity):
#         plot = QPSLDotChartData(capacity)
#         self.addItem(plot)
#         return plot

# class QPSLStaticOscilloscope(QPSLPlot):
#     def __init__(self, parent):
#         super(QPSLStaticOscilloscope, self).__init__(parent=parent)
#         self.m_main_plot = None

#     def set_plot(self, array):
#         if self.m_main_plot:
#             self.removeItem(self.m_main_plot)
#         self.m_main_plot = pyqtgraph.PlotDataItem()
#         self.m_main_plot.setData(array)
#         self.addItem(self.m_main_plot)

# class QPSLDynamicOscilloscope(QPSLPlot):
#     def __init__(self, parent, capacity, time_ratio):
#         super(QPSLDynamicOscilloscope, self).__init__(parent=parent)
#         self.m_main_plot = pyqtgraph.PlotDataItem()
#         self.addItem(self.m_main_plot)
#         self.set_downsample(20, False, 'subsample')
#         self.m_capacity = capacity
#         self.m_time_ratio = time_ratio
#         self.make_time_axis()
#         self.m_data = np.empty(shape=[capacity])
#         self.m_length = 0
#         self.set_switch(False)

#     def set_switch(self, b):
#         self.m_switch = b

#     def set_open(self):
#         self.set_switch(True)

#     def set_close(self):
#         self.set_switch(False)

#     def add_data(self, new_data):
#         if self.m_switch:
#             new_data_length = len(new_data)
#             if self.m_length+new_data_length <= self.m_capacity:
#                 self.m_data[self.m_length:self.m_length +
#                             new_data_length] = new_data
#             else:
#                 self.m_data[:-new_data_length] = self.m_data[new_data_length:]
#                 self.m_data[-new_data_length:] = new_data
#             self.m_length += new_data_length

#     def flush_data(self):
#         if self.m_length < self.m_capacity:
#             self.m_main_plot.setData(
#                 x=self.m_time_axis[:self.m_length], y=self.m_data[:self.m_length])
#             self.m_main_plot.setPos(0, 0)
#         else:
#             self.m_main_plot.setData(x=self.m_time_axis, y=self.m_data)
#             self.m_main_plot.setPos(
#                 (self.m_length-self.m_capacity)*self.m_time_ratio, 0)

#     def set_downsample(self, ds=None, auto=None, method=None):
#         self.m_main_plot.setDownsampling(ds, auto, method)

#     def set_capacity(self, capacity):
#         if capacity<=self.m_capacity:
#             self.m_capacity = capacity
#             self.m_data = self.m_data[-capacity:]
#         else:
#             self.m_capacity = capacity
#             self.m_data = np.hstack((np.empty(shape=[capacity-len(self.m_data),]),self.m_data))
#         self.make_time_axis()

#     def set_time_ratio(self, time_ratio):
#         self.m_time_ratio = time_ratio
#         self.make_time_axis()

#     def clear_data(self):
#         self.m_length = 0

#     def make_time_axis(self):
#         self.m_time_axis = np.arange(self.m_capacity)*self.m_time_ratio

# class QPSLDotChart(QPSLPlot):
#     def __init__(self, parent, capacity, time_ratio):
#         super(QPSLDotChart, self).__init__(parent=parent)
#         self.m_main_plot = pyqtgraph.PlotDataItem()
#         self.addItem(self.m_main_plot)
#         self.set_downsample(20, False, 'subsample')
#         self.m_capacity = capacity
#         self.m_time_ratio = time_ratio
#         self.m_data_x = np.empty(shape=[capacity])
#         self.m_data_y = np.empty(shape=[capacity])
#         self.m_length = 0
#         self.set_switch(False)

#     def set_switch(self, b):
#         self.m_switch = b

#     def set_open(self):
#         self.set_switch(True)

#     def set_close(self):
#         self.set_switch(False)

#     def add_data(self, data_x, data_y):
#         if self.m_switch:
#             new_data_length = len(data_x)
#             if self.m_length+new_data_length <= self.m_capacity:
#                 self.m_data_x[self.m_length:self.m_length +
#                               new_data_length] = data_x
#                 self.m_data_y[self.m_length:self.m_length +
#                               new_data_length] = data_y
#             else:
#                 self.m_data_x[:-
#                               new_data_length] = self.m_data_x[new_data_length:]
#                 self.m_data_x[-new_data_length:] = data_x
#                 self.m_data_y[:-
#                               new_data_length] = self.m_data_y[new_data_length:]
#                 self.m_data_y[-new_data_length:] = data_y
#             self.m_length += new_data_length

#     def flush_data(self):
#         if self.m_length < self.m_capacity:
#             self.m_main_plot.setData(x=self.m_data_x[:self.m_length],
#                                      y=self.m_data_y[:self.m_length])
#         else:
#             self.m_main_plot.setData(x=self.m_data_x, y=self.m_data_y)

#     def set_downsample(self, ds=None, auto=None, method=None):
#         self.m_main_plot.setDownsampling(ds, auto, method)

#     def set_capacity(self, capacity):
#         if capacity <= self.m_capacity:
#             self.m_capacity = capacity
#             self.m_data_x = self.m_data_x[-capacity:]
#             self.m_data_y = self.m_data_y[-capacity:]
#         else:
#             self.m_capacity = capacity
#             add = capacity-len(self.m_data_x)
#             self.m_data_x = np.hstack((np.empty(shape=[add]), self.m_data_x))
#             self.m_data_y = np.hstack((np.empty(shape=[add]), self.m_data_y))

#     def set_time_ratio(self, time_ratio):
#         self.m_time_ratio = time_ratio

#     def clear_data(self):
#         self.m_length = 0
