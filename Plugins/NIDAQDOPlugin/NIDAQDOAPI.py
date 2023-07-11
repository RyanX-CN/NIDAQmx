from QPSLClass.Base import*

class DAQmxDigitalOutputChannel(Structure):
    _fields_ = [('physical_line_name',c_char * 256)]

c_DAQmxDigitalOutputChannel_p = POINTER(DAQmxDigitalOutputChannel)

class DAQmxDigitalOutputTask(Structure):
    _fields_ =[('handle', c_void_p),
                ('channels', c_DAQmxDigitalOutputChannel_p),
                ('line_number', c_uint32),
                ('trigger_source', c_char * 1024), ('sample_rate', c_double),
                ('sample_mode', c_int32), ('sample_per_channel', c_int32),
                ('error_code', c_int32), ('error_buffer', c_char * 1024)]
    #TODO

c_DAQAnalogOutputTask_p = POINTER(DAQmxDigitalOutputTask)

c_int32_p = POINTER(c_int32)
c_uint32_p = POINTER(c_uint32)
c_double_p = POINTER(c_double)

try:
    _library = load_dll("QPSL_NIDAQDO.dll")
except BaseException as e:
    loading_error(e)
