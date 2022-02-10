# ScriptBox
个人脚本工具箱

使用的 `python` 版本皆为 `Python3`



## 文章

|标题|掘金|博客|公众号|
|-|-|-|-|
|iOS - 实现25秒内完成测试包出包|[【链接】](https://juejin.cn/post/7057177057637662728)|[【链接】](https://fullstackaction.com/pages/9b40a4/)|[【链接】](https://mp.weixin.qq.com/s/cZ8gUWuOt7gV74JBkqa8GQ)|



## 使用

### `push_dev_ipa.py`

> 功能：上传 `.app` 文件至蒲公英或 `fir`



一、目录结构：

```shell
项目（项目路径是到我这一级）
├── LXFCardsLayout
├── LXFCardsLayout.xcodeproj
├── LXFCardsLayout.xcworkspace
├── Podfile
├── Podfile.lock
├── Pods
├── fastlane
│   └── appack_set.json（配置文件）
└── script
    ├── build_time_conf.ini
    └── save_build_config.py
```

`save_build_config.py` 和 `appack_set.json` 按如上结构放好，也可以自行存放和调整脚本



二、配置

在项目中的 `Run Script` 添加命令

```shell
cd script
python3 save_build_config.py # 记录编译时配置
```

该操作的用意：在编译的过程中，将 `app` 包所在路径保持至 `script` 目录的 `build_time_conf.ini` 文件中，并使用 `build_dir_path` 做为其 `key`。

注：鉴于多人协作下，该 `build_time_conf.ini` 文件必定不可能相同，所以建议将该 `build_time_conf.ini` 文件添加至 `.gitignore` 中



三、脚本命令

```shell
push_dev_ipa.py -p "项目路径" -t "target名" --platform="pgyer或fir"

# platform 不传，则默认为 pgyer
# 如：
# python push_dev_ipa.py -p "/Users/lxf/Desktop/LXFCardsLayout/Example" -t "LXFCardsLayout_Example"
# python push_dev_ipa.py -p "/Users/lxf/Desktop/LXFCardsLayout/Example" -t "LXFCardsLayout_Example" --platform="fir"
```





## 配置文件

### `appack_set.json`

```json
{
  "pgyer_api_key": "蒲公英api_key",
  "pgyer_user_key": "蒲公英user_key",
  "pgyer_api_password": "安装密码",
  "fir_type": "ios",
  "fir_api_token": "fir的api_token"
}
```



## 作者

- LinXunFeng
- email: [linxunfeng@yeah.net](mailto:linxunfeng@yeah.net)
- Blogs: [全栈行动](https://fullstackaction.com/) | [掘金](https://juejin.im/user/58f8065e61ff4b006646c72d/posts) 


<img height="267.5" width="481.5" src="https://github.com/LinXunFeng/LinXunFeng/blob/master/static/img/FSAQR.png" />

