from QPSLClass.Base import *
from QPSLClass.QPSLObjectBase import QPSLObjectBase


class QPSLWorker(QObject, QPSLObjectBase):
    sig_thread_started = pyqtSignal()

    def __init__(self, parent: QObject, object_name: str):
        super().__init__(parent=None)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)
        self.m_thread = weakref.ref(QThread(self))
        self.moveToThread(self.m_thread())

    def init_and_connect_attr(self, signal: pyqtSignal, name: str,
                              initvalue: Any):
        setattr(self, name, initvalue)
        ref = weakref(self)

        def func(value):
            setattr(ref, name, value)

        connect_queued(signal, func)

    def start_thread(self):
        self.m_thread().start()
        self.sig_thread_started.emit()

    def stop_thread(self):
        self.m_thread().quit()
        self.m_thread().wait()
