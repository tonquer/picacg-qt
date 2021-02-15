# picacg-windows
用PyQt以及爬虫实现的哔咔漫画window客户端，已实现分类、搜索、收藏夹、下载、在线观看等功能。

## 功能介绍
1. 登陆分流，还原安卓端的三个分流入口
2. 分类，搜索，排行，收藏夹使用同一的逻辑，滚轮下滑自动加载下一页，双击打开
3. 漫画详情，章节列表和评论列表
4. 下载功能，目前按漫画名和章节建立目录，图片命名按数字递增
5. 看图模式，右键打开关闭工具栏，左右键翻页，上下键移动图片，Alt+滚轮放大缩小，再次点击铺满高度或者铺满宽度可以还原图片
6. waifu2x功能，可在设置中设置去噪、模型等，尽量使用GPU解码，如果显卡性能较差，建议关闭此功能。
7. 历史记录使用sqlite数据库，保存在history.db文件，与登陆帐号无关系。
8. 所有图片都会缓存到cache目录，后续应该会修改

## waifu2x功能
- waifu2x功能使用的是 ""https://github.com/nihui/waifu2x-ncnn-vulkan"" 改进而来，只保留了转码线程，去掉了文件加载改为由python传入字节流数据，去掉了文件保存改为转化成字节流传回给python处理，加了个中间层打包成pyd给python使用，lib目录下的waifu2x.pyd，代码目前在整理暂时未开源。
- 由于waifu2x-ncnn-vulkan编译参数和python混合编程有冲突的问题，所已只使用了代码，其中ncnn.lib,libwebp.lib是重新编译了libwebp和ncnn项目而来。
- 固定使用 models-cunet模型，缩放比目前固定2x(后续将根据图片自动调整)，去噪等级3（如果图片没有噪点可能会变得奇怪），转化线程是单独的c++线程，所以不会影响pyqt的性能。

## 如何使用
1. 下载最新的版本 ""https://github.com/tonquer/picacg-windows/releases""
2. 解压zip
3. 打开start.exe
4. 后续有更新，只需要下载最新版本覆盖原目录即可

## 如何编译
1. git clone https://github.com/tonquer/picacg-windows.git
2. pycharm打开，pip安装pyqt5, requests包
3. 将lib目录加入到sys.path或者，将lib下文件拷贝到python安装目录的DLLs目录下
4. pycharm运行start.py
5. 使用pyinstaller -F -w start.py 打包成exe

## 感谢以下项目
- https://github.com/nagadomi/waifu2x
- https://github.com/nihui/waifu2x-ncnn-vulkan
- https://github.com/webmproject/libwebp
- https://github.com/Tencent/ncnn
