# -*- coding: utf-8 -*-
# -*- author: LinXunFeng -*-

import getopt
import json
import os
import shutil
import sys
import time
from configparser import ConfigParser
from enum import Enum

from utils import file_util as FileUtil
from utils import upload_pgyer as PgyerUtil


class AppackSetKey(Enum):
    """appack_set的键"""
    PGYER_API_KEY = "pgyer_api_key"
    PGYER_USER_KEY = "pgyer_user_key"
    PGYER_PASSWORD_KEY = "pgyer_api_password"


def get_build_dir_path(config_ini_path):
    """获取项目的编译目录路径"""
    section_name = 'project'
    config = ConfigParser()
    config.read(config_ini_path)
    if not config.has_section(section_name):
        return ""
    else:
        return config.get(section_name, 'build_dir_path')


def get_build_config_ini_path(project_path):
    """获取build_conf.ini文件路径"""
    return os.path.join(project_path, 'script', 'build_time_conf.ini')


def get_pgyer_config(project_path):
    """获取蒲公英的相关配置"""
    config_set_json = os.path.join(project_path, 'fastlane', 'appack_set.json')
    json_data = json.loads(FileUtil.read_file(config_set_json))
    # print(json_data)
    pgyer_api_key = json_data[AppackSetKey.PGYER_API_KEY.value]
    pgyer_user_key = json_data[AppackSetKey.PGYER_USER_KEY.value]
    pgyer_password = json_data[AppackSetKey.PGYER_PASSWORD_KEY.value]
    return pgyer_api_key, pgyer_user_key, pgyer_password


def handle(project_path, target_name):
    app_name = target_name + '.app'

    config_ini_path = get_build_config_ini_path(project_path)
    build_dir_path = get_build_dir_path(config_ini_path)
    print('build_dir_path -- ', build_dir_path)
    app_path = os.path.join(build_dir_path, 'Build/Products/Debug-iphoneos', app_name)
    # print(app_path)
    # cur_path = os.path.abspath('.')
    script_path = os.path.join(project_path, 'script')
    temp_path = os.path.join(script_path, 'temp')
    payload_path = os.path.join(temp_path, 'Payload')
    payload_app_path = os.path.join(payload_path, app_name)

    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)  # 移除Payload
        time.sleep(1)  # 等删除完
    os.makedirs(payload_path)  # 创建Payload
    new_path = shutil.copytree(app_path, payload_app_path)
    # print(new_path)
    ipa_path = shutil.make_archive(payload_path, 'zip', temp_path)
    ipa_path = shutil.move(ipa_path, os.path.join(temp_path, target_name + '.ipa'))
    print(ipa_path)

    # 上传至蒲公英
    def payer_upload_callback():
        shutil.rmtree(temp_path)  # 删除temp目录

    pgyer_api_key, pgyer_user_key, pgyer_password = get_pgyer_config(project_path)
    PgyerUtil.upload_to_pgyer(ipa_path, pgyer_api_key, pgyer_user_key, password=pgyer_password, callbcak=payer_upload_callback)


if __name__ == "__main__":
    argv = sys.argv[1:]
    project_path = ""  # 项目路径
    target_name = ""  # target名称

    try:
        opts, args = getopt.getopt(argv, "p:t:", ["path=", "target_name="])
    except getopt.GetoptError:
        print('push_dev_ipa.py -p "项目路径" -t "target名"')
        sys.exit(2)

    print(opts)
    for opt, arg in opts:
        if opt in ["-p", "--path"]:
            project_path = arg
            if len(project_path) == 0:
                print('请输入项目的地址')
                sys.exit('请输入项目的地址')
        if opt in ["-t", "--target_name"]:
            target_name = arg

    # print(project_path)
    handle(project_path, target_name)
