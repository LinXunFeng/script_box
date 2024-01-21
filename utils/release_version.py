from enum import Enum
from utils import xcode_util as XcodeTool, file_util as FileTool


class ErrorCode(Enum):
    """错误代码"""
    NORMAL = 0  # 正常
    PARAMS_ERR = 1  # 入参错误
    UNKNOW = 2  # 未知
    PARSE_ERR = 3  # 解析


def fetch_project_version(
    xcodeproj_path,
    target_name,
):
    """
    获取主版本号
    :xcodeproj_path xcodeproj文件路径
    :target_name 项目Target名称
    """
    # 读取版本号
    build_setting_dict = XcodeTool.get_build_settings(xcodeproj_path, target_name)
    main_version_key = XcodeTool.BuildSettingKey.MARKETING_VERSION.value
    build_version_key = XcodeTool.BuildSettingKey.CURRENT_PROJECT_VERSION.value
    if main_version_key not in build_setting_dict:
        return None
    if build_version_key not in build_setting_dict:
        return None
    main_version = build_setting_dict[main_version_key]  # 主版本
    build_version = build_setting_dict[build_version_key]  # build版本
    return (main_version, build_version)
