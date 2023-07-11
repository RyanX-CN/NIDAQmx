from QPSLClass.Base import *
from QPSLClass.QPSLLogger import QPSLLogger


class QPSLObjectBase:
    add_log = QPSLLogger()
    add_debug = QPSLLogger(QPSL_LOG_LEVEL.DBG.value)
    add_info = QPSLLogger(QPSL_LOG_LEVEL.INF.value)
    add_warning = QPSLLogger(QPSL_LOG_LEVEL.WARN.value)
    add_error = QPSLLogger(QPSL_LOG_LEVEL.ERR.value)
    add_critical = QPSLLogger(QPSL_LOG_LEVEL.CRT.value)

    def __init__(self):
        self.m_qpsl_parent: weakref.ref[QPSLObjectBase] = None

    def to_delete(self):
        pass

    def set_QPSL_parent(self, qpsl_parent: QObject):
        if qpsl_parent is not None:
            self.m_qpsl_parent = weakref.ref(qpsl_parent)
        else:
            self.m_qpsl_parent = None

    def trace_path(self) -> str:
        names = []
        cur = self
        while cur is not None:
            names.append(QObject.objectName(cur))
            if cur.m_qpsl_parent:
                cur = cur.m_qpsl_parent()
            else:
                cur = None
        return '.'.join(names[::-1])

    def log_decorator(level=QPSL_LOG_LEVEL.DBG.value,
                      error_level=QPSL_LOG_LEVEL.ERR.value):

        def inner_wrap(func):
            para_count = get_function_para_count(func=func)

            def wrap_with_arg(self: QPSLObjectBase, *args, **kwargs):
                try:
                    if para_count > 1:
                        msg = "->into {0}.{1} ,args: {2} ...".format(
                            self.__class__.__name__,
                            get_function_name(func=func), ','.join(
                                map(
                                    lambda z: "{0} = {1}".format(
                                        z[0], simple_str(z[1])),
                                    itertools.chain(
                                        zip(
                                            get_function_para_names(
                                                func=func)[1:], args),
                                        kwargs.items()))))
                    else:
                        msg = "->into {0}.{1} ...".format(
                            self.__class__.__name__,
                            get_function_name(func=func))
                    self.add_log(msg=msg, level=level)
                    return func(self, *args, **kwargs)
                except BaseException as e:
                    self.add_log(msg=e,
                                 level=error_level,
                                 exc_info=True,
                                 stack_info=True)
                finally:
                    msg = "exit {0}.{1}".format(self.__class__.__name__,
                                                get_function_name(func=func))
                    self.add_log(msg=msg, level=level)

            return wrap_with_arg

        return inner_wrap
