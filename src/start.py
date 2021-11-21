# -*- coding: utf-8 -*-
"""第一个程序"""
import os
import sys
# macOS 修复
import time

from PySide2.QtWidgets import QDesktopWidget

from config import config
from config.setting import Setting
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str
from view.main.main_view import MainView

if sys.platform == 'darwin':
    # 确保工作区为当前可执行文件所在目录
    current_path = os.path.abspath(__file__)
    current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + '.')
    os.chdir(current_dir)
# else:
#     sys.path.insert(0, "lib")

try:
    from waifu2x_vulkan import waifu2x_vulkan
    config.CanWaifu2x = True
except Exception as es:
    config.CanWaifu2x = False
    if hasattr(es, "msg"):
        config.ErrorMsg = es.msg

from PySide6 import QtWidgets  # 导入PySide6部件

# 此处不能删除
import images_rc
from server.sql_server import DbBook as DbBook
DbBook()


if __name__ == "__main__":
    Log.Init()
    Setting.Init()
    Str.Reload()
    # QtWidgets.QApplication.testAttribute(Qt.HighDpiScaleFactorRoundingPolicy)
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Floor)
    app = QtWidgets.QApplication(sys.argv)  # 建立application对象
    try:
        QtOwner().SetApp(app)
        main = MainView()
    except Exception as es:
        Log.Error(es)
        sys.exit(-111)
    main.show()  # 显示窗体
    main.Init()
    sts = app.exec()
    main.Close()
    if config.CanWaifu2x:
        waifu2x_vulkan.stop()
    time.sleep(1)
    sys.exit(sts)  # 运行程序
