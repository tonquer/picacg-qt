# picacomic-windows
哔咔漫画window客户端，界面使用PySide2，已实现分类、搜索、收藏夹、下载、在线观看等功能。

## 功能介绍
1. 登陆分流，还原安卓端的三个分流入口
![image](https://github.com/tonquer/picacg-windows/blob/main/example/1.png)
2. 分类，搜索，排行，收藏夹使用同一的逻辑，滚轮下滑自动加载下一页，双击打开
3. 漫画详情，章节列表和评论列表
![image](https://github.com/tonquer/picacg-windows/blob/main/example/4.png)
4. 下载功能，目前按漫画名和章节建立目录，图片命名按数字递增
![image](https://github.com/tonquer/picacg-windows/blob/main/example/2.png)
5. 看图模式，右键打开关闭工具栏，左右键翻页，上下键移动图片，Alt+滚轮放大缩小，再次点击铺满高度或者铺满宽度可以还原图片
7. waifu2x功能，可在设置中设置去噪、模型等，尽量使用GPU解码，如果显卡性能较差，建议关闭此功能，下图（关闭/开启效果）。
![image](https://github.com/tonquer/picacg-windows/blob/main/example/5.png)![image](https://github.com/tonquer/picacg-windows/blob/main/example/6.png)


## waifu2x功能
- waifu2x功能使用的是 ""https://github.com/nihui/waifu2x-ncnn-vulkan"" 改进而来，只保留了转码线程，加了个中间层打包成pyd给python使用，lib目录下的waifu2x.pyd。
- 由于waifu2x-ncnn-vulkan编译参数和python混合编程有冲突的问题，所已只使用了代码，其中ncnn.lib,libwebp.lib是重新编译了libwebp和ncnn项目而来。
- 固定使用 models-cunet模型，缩放比目前固定2x，去噪等级3，线程数默认2，转化线程是单独的c++线程，不会影响pyqt的性能。

## 如何使用
1. 下载最新的版本 ""https://github.com/tonquer/picacg-windows/releases""
2. 解压zip
3. 打开start.exe
4. 后续有更新，只需要下载最新版本覆盖原目录即可

## 如何编译
1. git clone https://github.com/tonquer/picacg-windows.git
2. 安装Python3.7.9，pip安装PySide2, requests, Pillow包
3. 安装pycharm, 打开项目
4. pycharm运行start.py调试
5. 可使用pyinstaller -F -w start.py 打包成exe

## 感谢以下项目
- https://github.com/nagadomi/waifu2x
- https://github.com/nihui/waifu2x-ncnn-vulkan
- https://github.com/webmproject/libwebp
- https://github.com/Tencent/ncnn
