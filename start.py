# -*- coding: utf-8 -*-
"""第一个程序"""
import socket
import weakref

from PyQt5 import QtWidgets, QtCore, QtGui  # 导入PyQt5部件
import sys
sys.path.append("lib")
import waifu2x

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from src.qt.qtmain import BikaQtMainWindow
from src.util import Log

if __name__ == "__main__":
    Log.Init()
    app = QtWidgets.QApplication(sys.argv)  # 建立application对象
    # app.addLibraryPath("./resources")
    main = BikaQtMainWindow()

    main.show()  # 显示窗体
    main.Init()
    sys.exit(app.exec())  # 运行程序
    waifu2x.Stop()
