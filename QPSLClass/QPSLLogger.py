# NOSTABLE
import logging
import os
from datetime import datetime
from enum import Enum
from typing import Optional, Union


class QPSL_LOG_LEVEL(Enum):
    '''
    由于第三方库也有很多的输出，所以我们采用自定义等级
    姑且认为第三方库的日志，同等级下不如我们程序内部的日志重要。所以在同样的名字下，我们的等级值下比别人高 9
    type: ALL 可有可无的话
    QPSL_LOG_LEVEL.ALL = 9
    type: DBG 调试程序时需要看到的信息
    QPSL_LOG_LEVEL.DBG = 19
    type: INF 即使不调试程序也需要看到的信息
    QPSL_LOG_LEVEL.INF = 29
    type: WARN 做实验需要看到的关键提示，获取实验数据需要看到的信息
    QPSL_LOG_LEVEL.WARN = 39
    type: ERR 运行出错，需要注意查看
    QPSL_LOG_LEVEL.ERR = 49
    type: CRT 出现不可修复的错误
    QPSL_LOG_LEVEL.CRT = 49
    '''
    ALL = 9  # 任何信息
    DBG = 19  # 为了 debug
    INF = 29  # 普通信息
    WARN = 39  # 需要注意的信息
    ERR = 49  # 错误信息
    CRT = 59  # 崩溃信息


class ColoredConsoleHandler(logging.StreamHandler):
    color_dict = {
        QPSL_LOG_LEVEL.DBG.value: "\033[37m",  #white
        QPSL_LOG_LEVEL.INF.value: "\033[32m",  #green
        QPSL_LOG_LEVEL.WARN.value: "\033[33m",  #yellow
        QPSL_LOG_LEVEL.ERR.value: "\033[31m",  #red
        QPSL_LOG_LEVEL.CRT.value: "\033[35m",  #purple
    }
    color_state = True

    @classmethod
    def set_global_color_state(cls, state: bool):
        cls.color_state = state

    def format(self, record):
        if ColoredConsoleHandler.color_state:
            return "{0}{1}\033[0m".format(
                ColoredConsoleHandler.color_dict.get(record.levelno,
                                                     "\033[30m"),
                super().format(record))
        else:
            return super().format(record)


class QPSLLogger:
    __slots__ = "m_level"

    def __init__(self,
                 level: Optional[int] = None,
                 exc_info=True,
                 stack_info=True):
        self.m_level = level

    def __call__(self,
                 msg: object,
                 level: Optional[int] = None,
                 exc_info=False,
                 stack_info=False):
        if not level:
            level = self.m_level
        logging.getLogger().log(level=level,
                                msg=msg,
                                exc_info=exc_info,
                                stack_info=stack_info)


for level in QPSL_LOG_LEVEL._member_map_.values():
    logging.addLevelName(level.value, level.name)
if not os.path.exists("Log"):
    os.mkdir("Log")
__QPSL_file_handler = logging.FileHandler(
    filename=datetime.now().strftime("Log/%Y%m%d.txt"),
    mode="at",
    encoding="utf8",
    delay=False)
__QPSL_file_handler.setLevel(QPSL_LOG_LEVEL.ALL.value)
__QPSL_console_handler = ColoredConsoleHandler()
__QPSL_console_handler.setLevel(QPSL_LOG_LEVEL.INF.value)
__candidate_formats = [
    "{levelname:<8} {asctime} {message:<50}   {pathname}, line {lineno}",
    "{levelname:<10} {asctime} {message}",
]
logging.basicConfig(format=__candidate_formats[1],
                    style='{',
                    handlers=[__QPSL_file_handler, __QPSL_console_handler])
logging.getLogger().setLevel(logging.NOTSET)


def loading_info(message: str):
    logging.getLogger()._log(level=QPSL_LOG_LEVEL.INF.value,
                             msg=message,
                             args=())


def loading_warning(message: str):
    logging.getLogger()._log(level=QPSL_LOG_LEVEL.WARN.value,
                             msg=message,
                             args=())


def loading_error(message: str):
    logging.getLogger()._log(level=QPSL_LOG_LEVEL.ERR.value,
                             msg=message,
                             args=())


def set_console_log_level(level: QPSL_LOG_LEVEL):
    __QPSL_console_handler.setLevel(level=level.value)
