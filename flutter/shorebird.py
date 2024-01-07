import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import getopt
from enum import Enum
import xml.etree.ElementTree as ET

class ErrorCode(Enum):
    """错误代码"""
    NORMAL = 0  # 正常
    PARAMS_ERR = 1  # 入参错误
    UNKNOW = 2  # 未知
    PARSE_ERR = 3  # 解析

class Mode(Enum):
    """模式"""
    RELEASE = 0  # 发布
    PATCH = 1  # 补丁

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
    # 1. 读取主版本号
    file_path = os.path.join(project_path, 'app/src/main/AndroidManifest.xml')
    # 解析XML文件
    tree = ET.parse(file_path)
    # 获取根元素
    root = tree.getroot()
    version = None
    build_number = 1
    if root.tag == 'manifest':
        # print("version_name -- ", root.attrib)
        for attr in root.attrib:
          if attr.__contains__('versionName'):
            # 找到主版本号
            version = root.attrib[attr]
            print("version_name -- ", version)
          if attr.__contains__('versionCode'):
            # 找到主版本号
            build_number = root.attrib[attr]
            print("versionCode -- ", build_number)
    if version == None:
      print("未找到主版本号")
      sys.exit(ErrorCode.PARSE_ERR.value)
    # 2. 执行 release 命令
    # shorebird release aar -f --release-version 7.0.0+1
    command = ''
    version_build = str(version) + '+' + str(build_number)
    if mode == Mode.RELEASE:
      command = 'shorebird release aar -f --release-version ' + version_build
    elif mode == Mode.PATCH:
      command = 'shorebird patch aar -f --release-version ' + version_build
    else:
      print("未知模式")
      sys.exit(ErrorCode.PARAMS_ERR.value)
    print("command -- ", command)
    os.chdir(shell_path)
    print("当前作业路径 -- ", os.getcwd())
    os.system(command)

if __name__ == "__main__":
    argv = sys.argv[1:]
    target_name = None  # target名称
    mode = Mode.RELEASE  # 模式
    platform = Platform.ANDROID  # 平台

    try:
        opts, args = getopt.getopt(argv, "p:s:m:f:", ["path=", "shell=", "mode=", "platform="])
    except getopt.GetoptError:
        print('shorebird.py -p "原生项目路径" -s "Flutter壳项目路径" -m "模式(release|patch)" -f "平台(ios|android)"')
        sys.exit(1)

    for opt, arg in opts:
        if opt in ["-p", "--path"]:
            project_path = arg
            if len(project_path) == 0:
                print('请输入原生工程地址')
                sys.exit(ErrorCode.PARAMS_ERR.value)
        if opt in ["-s", "--shell"]:
            shell_path = arg
            if len(shell_path) == 0:
                print('请输入壳工程地址')
                sys.exit(ErrorCode.PARAMS_ERR.value)
        if opt in ["-m", "--mode"]:
            if (arg != "release" and arg != "patch"):
                print('请输入正确的模式')
                sys.exit(ErrorCode.PARAMS_ERR.value)
            if (arg == 'release'):
                mode = Mode.RELEASE
            else:
                mode = Mode.PATCH
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

# release
# python shorebird.py -p '安卓原生工程项目路径' -s 'Flutter壳项目路径' -m release -f android
# python shorebird.py -p 'iOS原生工程项目路径' -s 'Flutter壳项目路径' -m release -f ios

# patch
# python shorebird.py -p '安卓原生工程项目路径' -s 'Flutter壳项目路径' -m patch -f android
# python shorebird.py -p 'iOS原生工程项目路径' -s 'Flutter壳项目路径' -m patch -f ios