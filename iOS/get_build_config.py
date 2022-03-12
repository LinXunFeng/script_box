# -*- coding: UTF-8 -*-
# -*- author: LinXunFeng -*-
from configparser import ConfigParser


def get_config(config_ini_path, section_name, key):
    """获取项目的编译目录路径"""
    config = ConfigParser()
    config.read(config_ini_path)
    if not config.has_section(section_name):
        return None
    else:
        return config.get(section_name, key)

