# -*- coding: utf-8 -*-
"""
@author: Daniel
@contact: 511735184@qq.com
@file: __init__.py.py
@time: 2017/5/31 11:25
"""

import copy
from collections import OrderedDict

from utils.package_helper import import_mod
from utils.logger import system_log
from utils.i18n import gettext as _
from utils import RqAttrDict


class ModHandler(object):
    def __init__(self):
        self._env = None
        self._mod_list = list()
        self._mod_dict = OrderedDict()

    def set_env(self, environment):
        self._env = environment

        config = environment.config

        for mod_name in config.mod.__dict__:
            mod_config = getattr(config.mod, mod_name)
            if not mod_config.enabled:
                continue
            self._mod_list.append((mod_name, mod_config))

        for idx, (mod_name, user_mod_config) in enumerate(self._mod_list):
            if hasattr(user_mod_config, 'lib'):
                lib_name = user_mod_config.lib
            elif mod_name in SYSTEM_MOD_LIST:
                lib_name = "rqalpha.mod.rqalpha_mod_" + mod_name
            else:
                lib_name = "rqalpha_mod_" + mod_name
            system_log.debug(_(u"loading mod {}").format(lib_name))
            mod_module = import_mod(lib_name)
            if mod_module is None:
                del self._mod_list[idx]
                return
            mod = mod_module.load_mod()
            mod_config = RqAttrDict(copy.deepcopy(getattr(mod_module, "__config__", {})))
            mod_config.update(user_mod_config)
            setattr(config.mod, mod_name, mod_config)
            self._mod_list[idx] = (mod_name, mod_config)
            self._mod_dict[mod_name] = mod

        self._mod_list.sort(key=lambda item: getattr(item[1], "priority", 100))
        environment.mod_dict = self._mod_dict

    def start_up(self):
        for mod_name, mod_config in self._mod_list:
            self._mod_dict[mod_name].start_up(self._env, mod_config)

    def tear_down(self, *args):
        result = {}
        for mod_name, __ in reversed(self._mod_list):
            ret = self._mod_dict[mod_name].tear_down(*args)
            if ret is not None:
                result[mod_name] = ret
        return result


SYSTEM_MOD_LIST = [
    "sys_analyser",
    "sys_progress",
    "sys_funcat",
    "sys_risk",
    "sys_simulation",
    "sys_stock_realtime",
]
