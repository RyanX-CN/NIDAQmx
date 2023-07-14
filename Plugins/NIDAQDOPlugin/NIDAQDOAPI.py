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
    
    def init_task(self) -> int:
        _QPSL_DAQmxDO_init(pointer(self))
        if self.error_code:
            raise BaseException(bytes.decode(self.error_buffer,encoding='utf8'))
        return self.error_code
    
    def register_everyn_callback(self, everyn: int, callback: Callable,
                                 callback_data: c_void_p) -> int:
        _QPSL_DAQmxDO_register_everyn_callback(pointer(self), everyn, callback,
                                               callback_data)
        if self.error_code:
            raise BaseException(
                bytes.decode(self.error_buffer, encoding='utf8'))
        return self.error_code
    
    def register_done_callback(self, callback: Callable,
                               callback_data: c_void_p) -> int:
        _QPSL_DAQmxDO_register_done_callback(pointer(self), callback,
                                             callback_data)
        if self.error_code:
            raise BaseException(
                bytes.decode(self.error_buffer, encoding='utf8'))
        return self.error_code
    
    def write_data(self,arr2d:np.ndarray) ->Tuple[int,c_int32]:
        assert arr2d.shape[0] == self.line_number
        assert arr2d.shape[1] == self.sample_per_channel
        num_of_written = c_int32()
        arr = arr2d.reshape(arr2d.shape[0] *arr2d.shape[1])
        buffer = (c_double *len(arr))(*arr) 
        _QPSL_DAQmxWriteDigitalLines()

c_DAQmxDigitalOutputTask_p = POINTER(DAQmxDigitalOutputTask)

c_int32_p = POINTER(c_int32)
c_uint32_p = POINTER(c_uint32)
c_double_p = POINTER(c_double)

try:
    _library = load_dll("QPSL_NIDAQDO.dll")
except BaseException as e:
    loading_error(e)
try:
    _QPSL_DAQmxDO_init = getattr(_library, "QPSL_DAQmxDO_init")
    _QPSL_DAQmxDO_init.argtypes = [c_DAQmxDigitalOutputTask_p]
    _QPSL_DAQmxDO_init.restype = c_int32
except:
    loading_error("failed to load function {0}".format("QPSL_DAQmxDO_init"))
try:
    _QPSL_DAQmxDO_register_everyn_callback = getattr(
        _library, "QPSL_DAQmxDO_register_everyn_callback")
    _QPSL_DAQmxDO_register_everyn_callback.argtypes = [
        c_DAQmxDigitalOutputTask_p, c_uint32, c_void_p, c_void_p
    ]
    _QPSL_DAQmxDO_register_everyn_callback.restype = c_int32
except:
    loading_error("failed to load function {0}".format(
        "QPSL_DAQmxDO_register_everyn_callback"))
try:
    _QPSL_DAQmxDO_register_done_callback = getattr(
        _library, "QPSL_DAQmxDO_register_done_callback")
    _QPSL_DAQmxDO_register_done_callback.argtypes = [
        c_DAQmxDigitalOutputTask_p, c_void_p, c_void_p
    ]
    _QPSL_DAQmxDO_register_done_callback.restype = c_int32
except:
    loading_error("failed to load function {0}".format(
        "QPSL_DAQmxDO_register_done_callback"))
try:
    _QPSL_DAQmxWriteDigitalLines = getattr(_library,"QPSL_DAQmxWriteDigitalLines")
    _QPSL_DAQmxWriteDigitalLines.argtypes = [
        c_DAQmxDigitalOutputTask_p, c_int32_p, c_uint8
    ]
    _QPSL_DAQmxWriteDigitalLines.restype = c_int32
except:
    loading_error(
        "failed to load function {0}".format("QPSL_DAQmxWriteDigitalLines"))
