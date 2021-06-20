# -*- coding: utf-8 -*-
"""第一个程序"""
import sys
import os

import platform
# 确保工作区为当前可执行文件所在目录
if not (platform.system().upper() in ['WINDOWS', 'DARWIN', "LINUX"]):
    print(platform.system().upper())
    current_path = os.path.abspath(__file__)
    current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + '.')
    os.chdir(current_dir)

from conf import config
if not platform.system().upper() == 'DARWIN':
    sys.path.insert(0, "lib")

try:
    import waifu2x
    config.CanWaifu2x = True
except Exception as es:
    config.CanWaifu2x = False
    if hasattr(es, "msg"):
        config.ErrorMsg = es.msg

from PySide2 import QtWidgets  # 导入PySide2部件
from src.qt.qtmain import BikaQtMainWindow
from src.util import Log

if __name__ == "__main__":
    Log.Init()
    app = QtWidgets.QApplication(sys.argv)  # 建立application对象
    # app.addLibraryPath("./resources")
    main = BikaQtMainWindow()

    main.show()  # 显示窗体
    main.Init()
    sts = app.exec_()
    main.Close()
    if config.CanWaifu2x:
        waifu2x.stop()
    sys.exit(sts)  # 运行程序
