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
from save_build_config import BuildConfigSection, BuildConfigProjectKey
from get_build_config import get_config as GetBuildConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from utils import file_util as FileUtil
from utils import upload_pgyer as PgyerUtil
from utils import upload_fir as FirUtil


class UploadToPlatform(Enum):
    """上传至目的平台类型"""
    PGYER = "pgyer"
    FIR = "fir"


class AppackSetKey(Enum):
    """appack_set的键"""
    PGYER_API_KEY = "pgyer_api_key"
    PGYER_USER_KEY = "pgyer_user_key"
    PGYER_PASSWORD_KEY = "pgyer_api_password"
    FIR_TYPE_KEY = "fir_type"
    FIR_API_TOKEN_KEY = "fir_api_token"


def get_build_dir_path(config_ini_path):
    """获取项目的编译目录路径"""
    section_name = BuildConfigSection.PROJECT.value
    key = BuildConfigProjectKey.BUILD_DIR.value
    return GetBuildConfig(config_ini_path, section_name, key)


def get_configuration(config_ini_path):
    """获取项目的编译模式"""
    section_name = BuildConfigSection.PROJECT.value
    key = BuildConfigProjectKey.CONFIGURATION.value
    return GetBuildConfig(config_ini_path, section_name, key)


def get_build_config_ini_path(project_path):
    """获取build_conf.ini文件路径"""
    return os.path.join(project_path, 'script', 'build_time_conf.ini')


def get_config_dict(project_path):
    """获取appack_set.json文件路径"""
    config_set_json = os.path.join(project_path, 'fastlane', 'appack_set.json')
    return json.loads(FileUtil.read_file(config_set_json))


def get_pgyer_config(project_path):
    """获取蒲公英的相关配置"""
    json_data = get_config_dict(project_path)
    # print(json_data)
    pgyer_api_key = json_data[AppackSetKey.PGYER_API_KEY.value]
    pgyer_user_key = json_data[AppackSetKey.PGYER_USER_KEY.value]
    pgyer_password = json_data[AppackSetKey.PGYER_PASSWORD_KEY.value]
    return pgyer_api_key, pgyer_user_key, pgyer_password


def get_fir_config(project_path):
    """获取fir的相关配置"""
    json_data = get_config_dict(project_path)
    fir_type = json_data[AppackSetKey.FIR_TYPE_KEY.value]
    fir_api_token = json_data[AppackSetKey.FIR_API_TOKEN_KEY.value]
    return fir_type, fir_api_token


def handle(project_path, target_name, upload_to_platform):
    app_name = target_name + '.app'

    config_ini_path = get_build_config_ini_path(project_path)
    build_dir_path = get_build_dir_path(config_ini_path)
    # print('build_dir_path -- ', build_dir_path)
    app_path = os.path.join(build_dir_path, 'Build/Products/{}-iphoneos'.format(get_configuration(config_ini_path)), app_name)
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
    new_app_path = shutil.copytree(app_path, payload_app_path)
    # print(new_app_path)
    ipa_path = shutil.make_archive(payload_path, 'zip', temp_path)
    ipa_path = shutil.move(ipa_path, os.path.join(temp_path, target_name + '.ipa'))
    # print(ipa_path)

    # 上传完成回调
    def upload_complete_callback():
        shutil.rmtree(temp_path)  # 删除temp目录

    if upload_to_platform == UploadToPlatform.PGYER.value:  # 上传至蒲公英
        pgyer_api_key, pgyer_user_key, pgyer_password = get_pgyer_config(project_path)
        PgyerUtil.upload_to_pgyer(ipa_path, pgyer_api_key, pgyer_user_key, password=pgyer_password,
                                  callbcak=upload_complete_callback)
    elif upload_to_platform == UploadToPlatform.FIR.value:  # 上传至fir
        fir_type, fir_api_token = get_fir_config(project_path)
        FirUtil.upload_to_fir(app_path=new_app_path, ipa_path=ipa_path, api_token=fir_api_token, type=fir_type,
                              callbcak=upload_complete_callback)


if __name__ == "__main__":
    argv = sys.argv[1:]
    project_path = ""  # 项目路径
    target_name = ""  # target名称
    upload_to_platform = UploadToPlatform.PGYER.value  # 上传的平台

    try:
        opts, args = getopt.getopt(argv, "p:t:f:", ["path=", "target_name=", "platform="])
    except getopt.GetoptError:
        print('push_dev_ipa.py -p "项目路径" -t "target名" --platform="pgyer或fir"')
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
        if opt in ["-f", "--platform"]:
            upload_to_platform = arg

    # print(project_path)
    handle(project_path, target_name, upload_to_platform)
