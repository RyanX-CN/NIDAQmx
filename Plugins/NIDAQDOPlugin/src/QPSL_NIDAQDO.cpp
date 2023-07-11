#ifndef __QPSL_NIDAQDO__
#define __QPSL_NIDAQDO__
#include "NIDAQmx.h"
#include <stdio.h>
#include <stdlib.h>
#ifdef __cplusplus
extern "C" {
#endif
#define DLL_EXPORT __declspec(dllexport)
#define DAQmxErrChk(functionCall)                 \
    if (DAQmxFailed(error_code = (functionCall))) \
        return deal_err(error_code, error_buffer, len2);
#define DAQmxErrChk_task(functionCall)                  \
    if (DAQmxFailed(task->error_code = (functionCall))) \
        return deal_err_task(task);
struct DAQmxDigitalOutputChannel {
    char physical_line_name[256];
};
struct DAQmxDigitalOutputTask {
    TaskHandle handle;
    DAQmxDigitalOutputChannel *channels;
    uInt32 line_number;
    char trigger_source[1024];
    float64 sample_rate;
    int32 sample_mode;
    int32 sample_per_channel;
    int32 error_code;
    char error_buffer[1024];
};
int32 DLL_EXPORT QPSL_DAQmxGetErrorString(int32 error_code, char *error_buffer, uInt32 len) {
    return DAQmxGetErrorString(error_code, error_buffer, len);
}
int32 DLL_EXPORT QPSL_DAQmxGetExtendedErrorInfo(char *error_buffer, uInt32 len) {
    return DAQmxGetExtendedErrorInfo(error_buffer, len);
}
int32 deal_err(int32 error_code, char *error_buffer, uInt32 len) {
    if (DAQmxFailed(error_code)) {
        char temp[1024]{};
        DAQmxGetExtendedErrorInfo(temp, 1024);
        sprintf(error_buffer, "DAQmx Error: %s\n", temp);
    }
    return error_code;
}
int32 deal_err_task(DAQmxDigitalOutputTask *task) {
    if (DAQmxFailed(task->error_code)) {
        char temp[1024]{};
        DAQmxGetExtendedErrorInfo(temp, 1024);
        sprintf(task->error_buffer, "DAQmx Error: %s\n", temp);
    }
    if (task->handle != 0) {
        DAQmxStopTask(task->handle);
        DAQmxClearTask(task->handle);
        task->handle = 0;
    }
    return task->error_code;
}
int32 DLL_EXPORT QPSL_DAQmxGetDeviceList(char *name_list, uInt32 len, char *error_buffer, uInt32 len2) {
    int error_code;
    DAQmxErrChk(DAQmxGetSystemInfoAttribute(DAQmx_Sys_DevNames, name_list, len));
    return 0;
}
int32 DLL_EXPORT QPSL_DAQmxGetDOLineList(const char *device_name, char *name_list, uInt32 len, char *error_buffer, uInt32 len2) {
    int error_code;
    DAQmxErrChk(DAQmxGetDevDOLines(device_name, name_list, len));
    return 0;
}
int32 DLL_EXPORT QPSL_DAQmxGetDevTerminals(const char *device_name, char *terminal_list, uInt32 len, char *error_buffer, uInt32 len2) {
    int32 error_code;
    DAQmxErrChk(DAQmxGetDevTerminals(device_name, terminal_list, len));
    return 0;
}
int32 DLL_EXPORT QPSL_DAQmxDO_init(DAQmxDigitalOutputTask *task) {
    DAQmxErrChk_task(DAQmxCreateTask("", &task->handle));
    for (uInt32 i = 0; i < task->line_number; i++) {
        //DAQmx_Val_ChanPerLine: one line for one channel
        DAQmxErrChk_task(DAQmxCreateDOChan(task->handle, task->channels[i].physical_line_name, "", DAQmx_Val_ChanPerLine)); 
        //DAQmx_Val_ChanForAllLines: all lines for one channel
        //DAQmxErrChk_task(DAQmxCreateDOChan(task->handle, task->channels[i].physical_line_name, "", DAQmx_Val_ChanForAllLines)); 
    }
    DAQmxErrChk_task(DAQmxCfgSampClkTiming(task->handle, task->trigger_source, task->sample_rate, DAQmx_Val_Rising, task->sample_mode, task->sample_per_channel));
    return 0;
}
int32 DLL_EXPORT QPSL_DAQmxDO_start(DAQmxDigitalOutputTask *task) {
    DAQmxErrChk_task(DAQmxStartTask(task->handle));
    return 0;
}
int32 DLL_EXPORT QPSL_DAQmxDO_stop(DAQmxDigitalOutputTask *task) {
    DAQmxErrChk_task(DAQmxStopTask(task->handle));
    return 0;
}
int32 DLL_EXPORT QPSL_DAQmxDO_clear(DAQmxDigitalOutputTask *task) {
    DAQmxErrChk_task(DAQmxClearTask(task->handle));
    task->handle = 0;
    return 0;
}
//Write value to NI a digital output channel
int32 DLL_EXPORT QPSL_DAQmxWriteDigitaLines(DAQmxDigitalOutputTask *task,  int32 *num_of_written, uInt8 *buffer) {
    DAQmxErrChk_task(DAQmxWriteDigitalLines(task->handle, task->sample_per_channel, 0, 10.0, DAQmx_Val_GroupByChannel, buffer, num_of_written, NULL));
    return 0;
}
//Write value to NI a digital output port (port0:32bit, port1/2:8bit)
int32 DLL_EXPORT QPSL_DAQmxWriteDigitalU32(DAQmxDigitalOutputTask *task, int32 *num_of_written, uInt32 *buffer){
    DAQmxErrChk_task(DAQmxWriteDigitalU32(task->handle, task->sample_per_channel, 0, 10.0, DAQmx_Val_GroupByChannel, buffer, num_of_written, NULL));
}
int32 DLL_EXPORT QPSL_DAQmxWriteDigitslU8(DAQmxDigitalOutputTask *task, int32 *num_of_written, uInt8 *buffer) {
    DAQmxErrChk_task(DAQmxWriteDigitalU8(task->handle, task->sample_per_channel, 0, 10.0, DAQmx_Val_GroupByChannel, buffer, num_of_written, NULL));
    return 0;
}
int32 DLL_EXPORT QPSL_DAQmxAO_register_everyn_callback(DAQmxDigitalOutputTask *task, uInt32 n_samples, DAQmxEveryNSamplesEventCallbackPtr callback, void *callback_data) {
    DAQmxErrChk_task(DAQmxRegisterEveryNSamplesEvent(task->handle, DAQmx_Val_Transferred_From_Buffer, n_samples, 0, callback, callback_data));
    return 0;
}
int32 DLL_EXPORT QPSL_DAQmxAO_register_done_callback(DAQmxDigitalOutputTask *task, DAQmxDoneEventCallbackPtr callback, void *callback_data) {
    DAQmxErrChk_task(DAQmxRegisterDoneEvent(task->handle, 0, callback, callback_data));
    return 0;
}
int32 DLL_EXPORT QPSL_DAQmxGetBufOutputBufSize(DAQmxDigitalOutputTask *task, uInt32 *data) {
    DAQmxErrChk_task(DAQmxGetBufOutputBufSize(task->handle, data));
    return 0;
}
#ifdef __cplusplus
}
#endif
#endif