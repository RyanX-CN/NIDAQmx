from QPSLClass.Base import*

class DAQmxDigitalOutputChannel(Structure):
    pass

c_DAQmxDigitalOutputChannel_P = POINTER(DAQmxDigitalOutputChannel)

class DAQmxDigitalOutputTask(Structure):
    pass

c_DAQAnalogOutputTask_P = POINTER(DAQmxDigitalOutputTask)