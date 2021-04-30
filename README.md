# picacg-windows
- 哔咔漫画window客户端（现已支持Linux），界面使用QT。
- 该项目仅供技术研究使用，请勿用于其他用途。
- 如果觉得本项目对你有所帮助，请点个star关注，感谢支持
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
  - [ ] 头像
  - [ ] 传谕
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
- [ ] 游戏区
- [ ] 小电影
- [ ] 小里番
- [ ] 锅贴
- [ ] 画廊

## waifu2x功能
- waifu2x是用来提高图片分辨率和去噪点的功能， 介绍 "https://github.com/nagadomi/waifu2x"
- waifu2x-python，修改了waifu2x-ncnn-vulkan部分功能
- 由于bika限制上传图片的大小，所以部分图片（尤其是彩图）放在电脑大屏幕上观看会非常糊，所有通过waifu2x功能让图片在电脑上有更好的观感。
- waifu2x功能使用的是 "https://github.com/tonquer/waifu2x-ncnn-vulkan-python" 改进而来，打包成lib目录下的waifu2x.pyd。

## 如何使用
  ### Windows (测试使用win10)
  1. 下载最新的版本 https://github.com/tonquer/picacg-windows/releases
  2. 解压zip
  3. 打开start.exe
  4. 后续有更新，只需要下载最新版本覆盖原目录即可
  5. 如果无法初始化waifu2x，请更新显卡驱动，安装 [Vs运行库](https://download.visualstudio.microsoft.com/download/pr/366c0fb9-fe05-4b58-949a-5bc36e50e370/015EDD4E5D36E053B23A01ADB77A2B12444D3FB6ECCEFE23E3A8CD6388616A16/VC_redist.x64.exe)，如果还是无法启用，说明你的电脑不支持vulkan。
  ### Linux (测试使用deepin 20.2)
  1. 下载qt依赖， http://ftp.br.debian.org/debian/pool/main/x/xcb-util/libxcb-util1_0.4.0-1+b1_amd64.deb
  2. 安装依赖，sudo dpkg -i ./libxcb-util1_0.4.0-1+b1_amd64.deb
  3. 下载最新的版本 https://github.com/tonquer/picacg-windows/releases
  4. 解压tar -zxvf bika.tar.gz 
  5. cd bika && chmod +x start
  6. ./start
  7. 要想使用waifu2x请确定你的设备支持vulkan，然后安装vulkan驱动包，sudo apt install mesa-vulkan-drivers

## 如何编译
1. git clone https://github.com/tonquer/picacg-windows.git
2. 安装Python3.7.9，pip安装PySide2, requests, websocket-client包
3. 安装pycharm, 打开项目
4. pycharm运行start.py调试
5. 可使用pyinstaller -F -w start.py 打包成exe

## 感谢以下项目
- https://github.com/nagadomi/waifu2x
- https://github.com/nihui/waifu2x-ncnn-vulkan
- https://github.com/webmproject/libwebp
- https://github.com/Tencent/ncnn
- 如有任何问题，欢迎提ISSUE
