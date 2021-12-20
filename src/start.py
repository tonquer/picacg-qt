# -*- coding: utf-8 -*-
"""第一个程序"""
import os
import sys
# macOS 修复
import time

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QGuiApplication

from config import config
from config.setting import Setting
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str

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
    Setting.InitLoadSetting()
    indexV = Setting.ScaleLevel.GetIndexV()
    if indexV and indexV != "Auto":
        # if indexV == 100:
        #     QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Floor)
        # else:
            os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
            os.environ["QT_SCALE_FACTOR"] = str(indexV / 100)
    # os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    # print(QtWidgets.QApplication.testAttribute(Qt.AA_EnableHighDpiScaling))
    # print(QtWidgets.QApplication.testAttribute(Qt.AA_UseHighDpiPixmaps))
    # QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # print(QGuiApplication.highDpiScaleFactorRoundingPolicy())
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Floor)
    app = QtWidgets.QApplication(sys.argv)  # 建立application对象
    Str.Reload()

    Log.Warn("init scene ratio: {}".format(app.devicePixelRatio()))
    try:
        QtOwner().SetApp(app)
        from view.main.main_view import MainView
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
    time.sleep(2)
    print(sts)
    sys.exit(sts)  # 运行程序
