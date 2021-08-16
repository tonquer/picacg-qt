# picacg-windows(哔咔漫画) | [ehentai-windows(E绅士)](https://github.com/tonquer/ehentai-windows)  

[![GitHub](https://img.shields.io/github/license/tonquer/picacg-windows)](https://raw.githubusercontent.com/tonquer/picacg-windows/master/LICENSE.txt) 
[![GitHub](https://img.shields.io/github/workflow/status/tonquer/picacg-windows/windows-x64?label=Windows)](https://github.com/tonquer/picacg-windows/actions)
[![GitHub](https://img.shields.io/github/workflow/status/tonquer/picacg-windows/macos-x64?label=MacOS)](https://github.com/tonquer/picacg-windows/actions)
[![GitHub](https://img.shields.io/github/workflow/status/tonquer/picacg-windows/linux-x64?label=Linux)](https://github.com/tonquer/picacg-windows/actions)  
![Relese](https://img.shields.io/badge/Python-3.7.9%2B-brightgreen)
[![Relese](https://img.shields.io/github/v/release/tonquer/picacg-windows)](https://github.com/tonquer/picacg-windows/releases)
[![Relese](https://img.shields.io/github/downloads/tonquer/picacg-windows/latest/total)](https://github.com/tonquer/picacg-windows/releases)
[![Relese](https://img.shields.io/github/downloads/tonquer/picacg-windows/total)](https://github.com/tonquer/picacg-windows/releases)

- 哔咔漫画PC客户端（支持window、Linux和macOS），界面使用QT。
- 该项目仅供技术研究使用，请勿用于其他用途。
- 如果觉得本项目对你有所帮助，请点个star关注，感谢支持
- 如有使用中遇到问题，欢迎提ISSUE
## 功能
- [x] 主页
  - [x] 魔推荐
  - [x] 神推荐
  - [x] 随机本子
- [x] 分类
- [x] 用户
  - [x] 登陆
  - [x] 注册
  - [x] 打卡
  - [x] 收藏夹
  - [x] 头像
  - [x] 传谕
  - [ ] 修改信息
  - [ ] 通知
- [x] 搜索
  - [x] 热词
  - [x] 排序
  - [x] 封印
  - [x] 本地搜索
  - [ ] 分类
- [x] 排行榜
  - [x] 今日排行
  - [x] 7日排行
  - [x] 30日排行
  - [ ] 骑士榜
- [x] 聊天室
  - [x] 文字
  - [x] 图片
  - [ ] 语音
  - [x] 回复
  - [x] At
- [x] 漫画详情
  - [x] 章节
  - [x] 评论
  - [x] 看图
  - [x] waifu2x
- [x] 下载
  - [x] 按章节下载
  - [x] waifu2x
- [x] 留言板
  - [x] 子评论
  - [x] 回复
- [x] 历史记录
- [x] 游戏区
- [ ] 小电影
- [ ] 小里番
- [x] 锅贴
- [ ] 画廊

## 如何使用
  ### Windows (测试使用win10)
  1. 下载最新的版本 https://github.com/tonquer/picacg-windows/releases
  2. 解压zip
  3. 打开start.exe
  4. 后续有更新，只需要下载最新版本覆盖原目录即可
  5. 如果无法初始化waifu2x，请更新显卡驱动，安装 [Vs运行库](https://download.visualstudio.microsoft.com/download/pr/366c0fb9-fe05-4b58-949a-5bc36e50e370/015EDD4E5D36E053B23A01ADB77A2B12444D3FB6ECCEFE23E3A8CD6388616A16/VC_redist.x64.exe)，如果还是无法启用，说明你的电脑不支持vulkan。
  ### macOS (测试使用 macOS 10.15.7)
  1. 下载最新的版本 https://github.com/tonquer/picacg-windows/releases
  2. 解压 7z
  3. 将解压出的 PicACG 拖入访达 (Finder) 左侧侧栏的应用程序 (Applications) 文件夹中
  4. 从启动台 (Launchpad) 中找到并打开 PicACG
  #### 对于 M1 Mac 用户
  * 作者没有 Arm Mac, 所以没有办法提供已经打包好的应用程序
  * 如果您拥有 M1 Mac, 可以尝试参考下面的过程手动运行或者进行打包
  ### Linux (测试使用deepin 20.2)
  1. 下载qt依赖， http://ftp.br.debian.org/debian/pool/main/x/xcb-util/libxcb-util1_0.4.0-1+b1_amd64.deb
  2. 安装依赖，sudo dpkg -i ./libxcb-util1_0.4.0-1+b1_amd64.deb
  3. 下载最新的版本 https://github.com/tonquer/picacg-windows/releases
  4. 解压tar -zxvf bika.tar.gz 
  5. cd bika && chmod +x start
  6. ./start
  7. 要想使用waifu2x请确定你的设备支持vulkan，然后安装vulkan驱动包，sudo apt install mesa-vulkan-drivers

## 如何编译
  ### 使用Git Action编译
  1.查看编译结果[Git Action编译](https://github.com/tonquer/picacg-windows/actions)
  ### 其他
  1. git clone https://github.com/tonquer/picacg-windows.git
  2. 安装 Python 3.7+ (Mac 用户则只需要安装 [Xcode 12.4 及其命令行工具 (官方)](https://developer.apple.com/download/more/?name=Xcode%2012.4) ,安装后自带双架构 Python 3.8.2, 下载时需登录 iCloud 账号
  3. pip install -r requirements.txt
  4. 可以使用 pyinstaller -F -w start.py 打包成 exe
  5. 打包后将data models resources目录拷贝到dist目录
  ### 对于 macOS 用户
  ````bash
  pyinstaller --clean --log-level TRACE --onedir --name PicACG \
              --add-binary waifu2x.so:. --hidden-import PySide2 --hidden-import requests \
              --hidden-import urllib3 --hidden-import websocket-client --hidden-import pillow \
              --hidden-import conf --hidden-import resources --hidden-import src \
              --hidden-import src.index --hidden-import src.qt --hidden-import src.qt.chat \
              --hidden-import src.qt.com --hidden-import src.qt.download \
              --hidden-import src.qt.main --hidden-import src.qt.menu \
              --hidden-import src.qt.read --hidden-import src.qt.struct --hidden-import src.qt.game \
              --hidden-import src.qt.user --hidden-import src.qt.util --hidden-import src.server \
              --hidden-import src.user --hidden-import src.util --hidden-import ui \
              --hidden-import qss --strip --windowed -i Icon.icns \
              start.py
  rm -rf dist/PicACG
  cp -avf data example models resources dist/PicACG.app/Contents/MacOS
  rm -f dist/PicACG.app/Contents/MacOS/resources/*.py
  ````
  * 打包完成以后可以在 dist 目录下找到应用程序 (.app)

## 关于代理问题
  1. 如果你没有代理软件，请在设置中http代理一栏，取消勾选代理，尝试使用分流2，3连接。
  2. 如果你有代理软件，请在设置中http代理一栏，勾选代理，并且填入你软件提供的代理地址比如  
  v2ray可能是http://127.0.0.1:10809  
  shadowsocks可能是http://127.0.0.1:1080  

## 界面

* 登录
![登录](example/登录.gif)

* 搜索
![搜索](example/搜索.gif)

* 漫画详情
![漫画详情](example/漫画详情.gif)

* 下载
![下载](example/下载.gif)

* 看图
![看图](example/看图.gif)

* waifu2x
![waifu2x](example/waifu2x.gif)

## 感谢以下项目
  ### waifu2x功能
  - https://github.com/nagadomi/waifu2x
  - https://github.com/nihui/waifu2x-ncnn-vulkan
  - https://github.com/tonquer/waifu2x-ncnn-vulkan-python
  ### Qt功能
  - https://github.com/PyQt5/PyQt
  - https://github.com/PyQt5/PyQtClient
  ### Qt皮肤
  - https://github.com/satchelwu/QSS-Skin-Builder
  ### Qt实现平滑滚动
  - https://github.com/zhiyiYo/Groove
