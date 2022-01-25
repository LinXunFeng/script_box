# -*- coding: UTF-8 -*-
# -*- author: LinXunFeng -*-
import os
from configparser import ConfigParser


def handle_build_config():
    """保存编译时的一些配置"""
    build_dir_path = os.getenv("BUILD_DIR")  # 编译地址
    if build_dir_path is None:
        return
    
    build_str_index = build_dir_path.find('Build/')
    if build_str_index is not None:
        build_dir_path = build_dir_path[0:build_str_index]
    print(build_dir_path)
    save_config('build_dir_path', build_dir_path)


def save_config(key, value):
    """
    保存配置
    :param key: 键
    :param value: 值
    :return:
    """
    section_name = 'project'
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
