# NOSTABLE
import json
import os

if not os.path.exists("Config"):
    os.mkdir("Config")
__QPSL_config_path = "Config/main_conf.json"
with open(__QPSL_config_path, "rt") as f:
    __QPSL_config_dict: dict = json.load(f)


def configer_get(key):
    return __QPSL_config_dict.get(key)


def configer_set(key, value):
    __QPSL_config_dict.update({key: value})


def configer_getset(key, value):
    if key not in __QPSL_config_dict:
        __QPSL_config_dict.update({key: value})
    return __QPSL_config_dict.get(key)


def configer_write():
    with open(__QPSL_config_path, "wt") as f:
        json.dump(__QPSL_config_dict, f, indent=4)