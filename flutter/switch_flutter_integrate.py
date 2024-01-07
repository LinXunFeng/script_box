import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import getopt
from enum import Enum
from utils import file_util as FileTool


class ErrorCode(Enum):
    """错误代码"""
    NORMAL = 0  # 正常
    PARAMS_ERR = 1  # 入参错误
    UNKNOW = 2  # 未知
    PARSE_ERR = 3  # 解析

class Mode(Enum):
    """集成模式"""
    BINARY = 0  # 二进制
    SOURCE = 1  # 源码

class Platform(Enum):
    """平台"""
    ANDROID = 0  # 安卓
    IOS = 1  # iOS

def handle_ios():
    """
    处理iOS项目
    """
    pass

def handle_android():
    """
    处理安卓项目
    """
    print("项目路径：", project_path, "编译模式：", flutter_build_mode)
    is_binary = flutter_build_mode == Mode.BINARY
    comment_symbol = '//' # 注释符号
    # 1. 修改 build.gradle.kts
    file_path = os.path.join(project_path, 'build.gradle.kts')
    common_str = '        maven(url = "../../flutter_module/release")'
    target_str = (comment_symbol if is_binary else "") + common_str
    final_str = ("" if is_binary else comment_symbol) + common_str
    print("target_str -- ", target_str)
    print("final_str -- ", final_str)
    FileTool.replace(file_path, target_str, final_str)
    common_str = '        maven(url = "https://download.shorebird.dev/download.flutter.io")'
    target_str = (comment_symbol if is_binary else "") + common_str
    final_str = ("" if is_binary else comment_symbol) + common_str
    print("target_str -- ", target_str)
    print("final_str -- ", final_str)
    FileTool.replace(file_path, target_str, final_str)

    # 2. 修改 flutter_settings.gradle
    file_path = os.path.join(project_path, 'flutter_settings.gradle')
    target_str = '//evaluate(new File(\n//        settingsDir,\n//        "../flutter_module/.android/include_flutter.groovy"\n//))'
    final_str = 'evaluate(new File(\n        settingsDir,\n        "../flutter_module/.android/include_flutter.groovy"\n))'
    FileTool.replace(file_path, final_str if is_binary else target_str , target_str if is_binary else final_str)

    # 3. 修改 app/build.gradle.kts
    file_path = os.path.join(project_path, 'app', 'build.gradle.kts')
    common_str = '    implementation(project(LocalLib.flutter))'
    target_str = ("" if is_binary else comment_symbol) + common_str
    final_str = (comment_symbol if is_binary else "") + common_str
    print("target_str -- ", target_str)
    print("final_str -- ", final_str)
    FileTool.replace(file_path, target_str, final_str)
    common_str = '    releaseImplementation("com.lxf.flutter_modules:flutter_release:1.0")'
    target_str = (comment_symbol if is_binary else "") + common_str
    final_str = ("" if is_binary else comment_symbol) + common_str
    print("target_str -- ", target_str)
    print("final_str -- ", final_str)
    FileTool.replace(file_path, target_str, final_str)


if __name__ == "__main__":
    argv = sys.argv[1:]
    target_name = None  # target名称
    flutter_build_mode = Mode.BINARY  # flutter编译模式
    platform = Platform.ANDROID  # 平台

    try:
        opts, args = getopt.getopt(argv, "p:m:f:", ["path=", "mode=", "platform="])
    except getopt.GetoptError:
        print('switch_flutter_integrate.py -p "项目路径" -m "模式(binary|source)" -f "平台(ios|android)"')
        sys.exit(1)

    for opt, arg in opts:
        if opt in ["-p", "--path"]:
            project_path = arg
            if len(project_path) == 0:
                print('请输入原生工程地址')
                sys.exit(ErrorCode.PARAMS_ERR.value)
        if opt in ["-m", "--mode"]:
            if (arg != "binary" and arg != "source"):
                print('请输入正确的模式')
                sys.exit(ErrorCode.PARAMS_ERR.value)
            if (arg == 'binary'):
                flutter_build_mode = Mode.BINARY
            else:
                flutter_build_mode = Mode.SOURCE
        if opt in ["-f", "--platform"]:
            if (arg != "ios" and arg != "android"):
                print('请输入正确的平台')
                sys.exit(ErrorCode.PARAMS_ERR.value)
            if (arg == 'ios'):
                platform = Platform.IOS
            else:
                platform = Platform.ANDROID

    if platform == Platform.IOS:
        handle_ios()
    else:
        handle_android()

# 二进制依赖
# python switch_flutter_integrate.py -p '安卓原生工程项目路径' -m 'binary' -f 'android'
# python switch_flutter_integrate.py -p 'iOS原生工程项目路径' -m 'binary' -f 'ios'

# 源码依赖
# python switch_flutter_integrate.py -p '安卓原生工程项目路径' -m 'source' -f 'android' 
# python switch_flutter_integrate.py -p '安卓原生工程项目路径' -m 'source' -f 'ios'