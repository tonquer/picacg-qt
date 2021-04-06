# -*- coding: utf-8 -*-
"""第一个程序"""
import sys

from conf import config
sys.path.append("lib")
try:
    import waifu2x
    config.CanWaifu2x = True
except Exception as es:
    config.CanWaifu2x = False

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
    if config.CanWaifu2x:
        waifu2x.Stop()
    sys.exit(sts)  # 运行程序
