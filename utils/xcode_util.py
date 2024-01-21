import subprocess
from enum import Enum, unique
from pbxproj import XcodeProject


@unique
class BuildSettingKey(Enum):
    MARKETING_VERSION = "MARKETING_VERSION"
    CURRENT_PROJECT_VERSION = "CURRENT_PROJECT_VERSION"
    ARCHS = "ARCHS"
    DART_DEFINES = "DART_DEFINES"
    OTHER_SWIFT_FLAGS = "OTHER_SWIFT_FLAGS"


def get_build_settings(proj_path, target=None, scheme=None):
    """
    :proj_path xcodeproj文件的路径
    :target Target名称
    :scheme Scheme名称
    :desc 以字典的形式获取build_settings
            xcodebuild -project "xxx/Test.xcodeproj" -scheme schemeName -target targetName -showBuildSettings
    """
    project_param = (" -project %s" %proj_path) if proj_path is not None else ""
    target_param = (" -target %s" % target) if target is not None else ""
    scheme_param = (" -scheme %s" % scheme) if scheme is not None else ""
    command = "xcodebuild%s%s%s -showBuildSettings" % (project_param, target_param, scheme_param)
    status, output = subprocess.getstatusoutput(command)
    arr_param = output.split("\n")
    dic_param = {}

    for param in arr_param:
        if " = " in param:
            split_list = param.split(" = ")
            if len(split_list) != 2:
                continue
            key, value = split_list
            key = key.strip()
            value = value.strip()
            dic_param[key] = value
        else:
            pass

    return dic_param


def get_build_configurations(proj_path, target):
    """
    获取 Build Configurations
    :proj_path xcodeproj文件的路径
    :target Target名称
    """
    project = XcodeProject.load(proj_path)
    return project.get_build_configurations_by_target(target)  # ['Debug', 'Release', 'Test']


def get_build_settings_obj(
    proj_path, 
    target, 
    configuration='Debug', 
    project=None
):
    """
    获取 BuildSetting
    :proj_path xcodeproj文件的路径
    :target Target名称
    :configuration Build Configuration
    :project 加载好的 XcodeProject 对象
    """
    if (project is None):
        project = XcodeProject.load(proj_path)
    target = project.get_target_by_name(target)
    if target is None:
        return None;
    
    build_configuration_list = project.objects[target.buildConfigurationList]
    target_build_configurations = build_configuration_list['buildConfigurations']

    for build_configuration in target_build_configurations:
        build_configuration_obj = project.objects[build_configuration]
        if build_configuration_obj is not None:
            if build_configuration_obj.name == configuration:
                return build_configuration_obj.buildSettings
    return None;

def set_build_settings_obj(
    key,
    value,
    proj_path, 
    target, 
    configuration='Debug', 
    project=None
):
    """
    设置 BuildSetting
    :proj_path xcodeproj文件的路径
    :target Target名称
    :configuration Build Configuration
    :project 加载好的 XcodeProject 对象
    """
    if (project is None):
        project = XcodeProject.load(proj_path)
    build_settings = get_build_settings_obj(
        proj_path=proj_path, 
        target=target, 
        configuration=configuration, 
        project=project
    )
    if build_settings is None: return
    build_settings[key] = value
    project.save()
    