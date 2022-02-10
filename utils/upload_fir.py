import sys
import os
import requests
import json
from .plist_util import PlistUtil


def upload_to_fir(app_path, ipa_path, api_token, type='ios', callbcak=None):
    """
    上传到蒲公英
    :param app_path: app文件路径
    :param ipa_path: ipa文件路径
    :param api_token: fir 的 api token
    :param type:
    """
    plist_path = os.path.join(app_path, "info.plist")
    plist = PlistUtil(plist_path)
    bundle_id = plist.getValueForKey("CFBundleIdentifier").decode().replace('\n', '')
    app_name = plist.getValueForKey("CFBundleName").decode().replace('\n', '')
    version = plist.getValueForKey("CFBundleShortVersionString").decode().replace('\n', '')
    build = plist.getValueForKey("CFBundleVersion").decode().replace('\n', '')

    binary = get_fir_params(type=type, bundle_id=bundle_id, api_token=api_token)
    if binary is None:
        sys.exit('获取请求参数失败，请检查配置')
    key = binary['key']
    token = binary['token']
    upload_url = binary['upload_url']

    file = {
        'file': open(ipa_path, 'rb')
    }
    param = {
        "key": key,  # binary字段对应的key
        "token": token,  # binary字段对应的token
        "x:name": app_name,  # 应用名称
        "x:version": version,  # 版本号
        "x:build": build,  # Build 号
        # "x:changelog": '更新日志'
    }
    print("上传至fir中....")
    r = requests.post(upload_url, files=file, data=param)
    if r.status_code == requests.codes.ok:
        # result = r.json()
        # print(result)
        print("上传成功")
    else:
        print('HTTPError,Code:'+r.status_code)

    if callbcak is not None:
        callbcak()


def get_fir_params(type, bundle_id, api_token):
    data = {
        'type': type,
        'bundle_id': bundle_id,
        'api_token': api_token,
    }
    req = requests.post('http://api.bq04.com/apps', data=data)
    result = req.json()
    # print(json.dumps(result))
    if req.status_code == requests.codes.created:
        return result["cert"]["binary"]
    else:
        print('HTTPError,Code:'+req.status_code)
