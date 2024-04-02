# 哔咔漫画

## 简体中文 | [English](README_EN.md)

[![GitHub](https://img.shields.io/github/license/tonquer/picacg-qt)](https://raw.githubusercontent.com/tonquer/picacg-qt/master/LICENSE.txt)
[![GitHub](https://img.shields.io/github/workflow/status/tonquer/picacg-qt/CI?label=CI)](https://github.com/tonquer/picacg-qt/actions)
![Relese](https://img.shields.io/badge/Python-3.7.9%2B-brightgreen)
[![Relese](https://img.shields.io/github/v/release/tonquer/picacg-qt)](https://github.com/tonquer/picacg-qt/releases)
![Relese](https://img.shields.io/github/downloads/tonquer/picacg-qt/total)

- 哔咔漫画PC客户端（支持window、Linux和macOS），界面使用QT
- 该项目仅供技术研究使用，请勿用于其他用途
- 如果觉得本项目对你有所帮助，请点个star关注，感谢支持
- 如有使用中遇到问题，欢迎提ISSUE

## 功能
- 已实现哔咔漫画大部分功能
- 支持看图和下载

## 如何使用
  ### Windows (测试使用win10)
  1. 下载最新的版本 https://github.com/tonquer/picacg-qt/releases
  2. 解压zip
  3. 打开start.exe
  4. 后续有更新，只需要下载最新版本覆盖原目录即可
  5. 如果无法初始化Waifu2x, DLL错误, 请安装 [Vs运行库](https://download.visualstudio.microsoft.com/download/pr/366c0fb9-fe05-4b58-949a-5bc36e50e370/015EDD4E5D36E053B23A01ADB77A2B12444D3FB6ECCEFE23E3A8CD6388616A16/VC_redist.x64.exe), [Vulkan运行库](https://sdk.lunarg.com/sdk/download/1.3.239.0/windows/VulkanRT-1.3.239.0-Installer.exe)

  ### macOS (测试使用 macOS 10.15.7)
  1. 下载最新的版本 https://github.com/tonquer/picacg-qt/releases
  2. 解压 7z
  3. 将解压出的 PicACG 拖入访达 (Finder) 左侧侧栏的应用程序 (Applications) 文件夹中
  4. 从启动台 (Launchpad) 中找到并打开 PicACG
  #### 对于 M1 Mac 用户
  * 作者没有 Arm Mac, 所以没有办法提供已经打包好的应用程序
  * 如果您拥有 M1 Mac, 可以尝试参考下面的过程手动运行或者进行打包

  ### Linux (测试使用deepin 20.2)
  1. 下载qt依赖， http://ftp.br.debian.org/debian/pool/main/x/xcb-util/libxcb-util1_0.4.0-1+b1_amd64.deb
  2. 安装依赖，sudo dpkg -i ./libxcb-util1_0.4.0-1+b1_amd64.deb
  3. 下载最新的版本 https://github.com/tonquer/picacg-qt/releases
  4. 解压tar -zxvf bika.tar.gz 
  5. cd bika && chmod +x start
  6. ./start
  7. 要想使用waifu2x请确定你的设备支持vulkan，然后安装vulkan驱动包，sudo apt install mesa-vulkan-drivers

## 关于代理问题
  请看说明 https://github.com/tonquer/picacg-qt/discussions/48

## 如何编译
  ### 使用Git Actions编译
  1. 查看编译结果[Git Actions编译](https://github.com/tonquer/picacg-qt/actions)

## 我的其他项目
 [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=tonquer&repo=JMComic-qt)](https://github.com/tonquer/JMComic-qt)  
 [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=tonquer&repo=ehentai-qt)](https://github.com/tonquer/ehentai-qt)  
 
## 界面

* 登录

* 搜索

* 漫画详情

* 下载

* 看图

* waifu2x

## 感谢以下项目
  ### waifu2x功能
   [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=nagadomi&repo=waifu2x)](https://github.com/nagadomi/waifu2x)  
   [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=nihui&repo=waifu2x-ncnn-vulkan)](https://github.com/nagadomi/waifu2x-ncnn-vulkan)  
   [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=tonquer&repo=waifu2x-vulkan)](https://github.com/tonquer/waifu2x-vulkan)  
  ### Qt功能
   [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=PyQt5&repo=PyQt)](https://github.com/PyQt5/PyQt)  
   [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=PyQt5&repo=PyQtClient)](https://github.com/PyQt5/PyQtClient)  
  ### Qt皮肤
   [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=UN-GCPDS&repo=qt-material)](https://github.com/UN-GCPDS/qt-material)  
   [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=satchelwu&repo=QSS-Skin-Builder)](https://github.com/satchelwu/QSS-Skin-Builder)  
  ### Qt实现平滑滚动
   [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=zhiyiYo&repo=Groove)](https://github.com/zhiyiYo/Groove)
