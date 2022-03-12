# -*- coding: UTF-8 -*-
# -*- author: LinXunFeng -*-
import os
import enum
from configparser import ConfigParser


class BuildConfigSection(enum.Enum):
    PROJECT = 'project'


class BuildConfigProjectKey(enum.Enum):
    BUILD_DIR = 'build_dir_path'
    CONFIGURATION = 'configuration'


def handle_build_config():
    """保存编译时的一些配置"""
    build_dir_path = os.getenv("BUILD_DIR")  # 编译地址
    if build_dir_path is None:
        return
    
    build_str_index = build_dir_path.find('Build/')
    if build_str_index is not None:
        build_dir_path = build_dir_path[0:build_str_index]
    print(build_dir_path)
    save_config(BuildConfigProjectKey.BUILD_DIR.value, build_dir_path)

    configuration = os.getenv("CONFIGURATION")  # 编译模式
    print(configuration)
    save_config(BuildConfigProjectKey.CONFIGURATION.value, configuration)


def save_config(key, value):
    """
    保存配置
    :param key: 键
    :param value: 值
    :return:
    """
    section_name = BuildConfigSection.PROJECT.value
    config_file_name = 'build_time_conf.ini'
    config = ConfigParser()
    config.read(config_file_name)
    if not config.has_section(section_name):
        config.add_section(section_name)
    config.set(section_name, key, value)
    with open(config_file_name, 'w') as f:
        config.write(f)


if __name__ == '__main__':
    handle_build_config()
