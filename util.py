# -*- coding: utf-8 -*-
"""
@author: Daniel
@contact: 511735184@qq.com
@file: util.py
@time: 2017/5/31 16:08
"""
import os
import codecs
import json
import yaml

from utils.i18n import gettext


def load_config(config_path, loader=yaml.Loader):
    if config_path is None:
        return {}
    if not os.path.exists(config_path):
        raise RuntimeError(gettext(u"config.yml not found in {config_path}").format(config_path))
    if ".json" in config_path:
        with codecs.open(config_path, encoding="utf-8") as f:
            json_config = f.read()
        config = json.loads(json_config)
    else:
        with codecs.open(config_path, encoding="utf-8") as stream:
            config = yaml.load(stream, loader)
    return config

if __name__ == '__main__':
    config = load_config(config_path='config.yml')
    print(config)
