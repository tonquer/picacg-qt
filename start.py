# -*- coding: utf-8 -*-
"""第一个程序"""
import sys
import os

from conf import config

# macOS 修复
import time

from PySide6.QtGui import Qt, QGuiApplication

if sys.platform == 'darwin':
    # 确保工作区为当前可执行文件所在目录
    current_path = os.path.abspath(__file__)
    current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + '.')
    os.chdir(current_dir)
# else:
#     sys.path.insert(0, "lib")

try:
    import waifu2x_vulkan
    config.CanWaifu2x = True
except Exception as es:
    config.CanWaifu2x = False
    if hasattr(es, "msg"):
        config.ErrorMsg = es.msg

from PySide6 import QtWidgets  # 导入PySide6部件
from src.qt.qtmain import BikaQtMainWindow
from src.util import Log

# 此处不能删除
from src.server.sql_server import DbBook as DbBook
DbBook()


if __name__ == "__main__":
    # TODO 调缩放后 错位，临时处理
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Floor)
    # QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    Log.Init()
    app = QtWidgets.QApplication(sys.argv)  # 建立application对象
    try:
        main = BikaQtMainWindow(app)
    except Exception as es:
        Log.Error(es)
        sys.exit(-111)
    main.show()  # 显示窗体
    main.Init()
    sts = app.exec()
    main.Close()
    if config.CanWaifu2x:
        waifu2x.stop()
    time.sleep(1)
    sys.exit(sts)  # 运行程序