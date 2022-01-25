import requests


def upload_to_pgyer(path, api_key, user_key, install_type=2, password='', update_description='', callbcak=None):
    """
    上传到蒲公英
    :param path: 文件路径
    :param api_key: API Key
    :param user_key: User Key
    :param install_type: 应用安装方式，值为(1,2,3)。1：公开，2：密码安装，3：邀请安装。默认为1公开
    :param password: App安装密码
    :param update_description:
    :return: 版本更新描述
    """
    files = {'file': open(path, 'rb')}
    headers = {'enctype': 'multipart/form-data'}
    payload = {
        'uKey': user_key,
        '_api_key': api_key,
        'installType': install_type,
        'password': password,
        'updateDescription': update_description,
    }
    print("上传中....")
    r = requests.post('https://www.pgyer.com/apiv2/app/upload', data=payload, files=files, headers=headers)
    if r.status_code == requests.codes.ok:
        # result = r.json()
        # print(result)
        print("上传成功")
    else:
        print('HTTPError,Code:'+r.status_code)

    if callbcak is not None:
        callbcak()

