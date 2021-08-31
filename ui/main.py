# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(353, 223)
        self.actionsetting = QAction(MainWindow)
        self.actionsetting.setObjectName(u"actionsetting")
        self.actionabout = QAction(MainWindow)
        self.actionabout.setObjectName(u"actionabout")
        self.actionimg_convert = QAction(MainWindow)
        self.actionimg_convert.setObjectName(u"actionimg_convert")
        self.actionproxy = QAction(MainWindow)
        self.actionproxy.setObjectName(u"actionproxy")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 353, 26))
        self.menusetting = QMenu(self.menubar)
        self.menusetting.setObjectName(u"menusetting")
        self.menuabout = QMenu(self.menubar)
        self.menuabout.setObjectName(u"menuabout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menusetting.menuAction())
        self.menubar.addAction(self.menuabout.menuAction())
        self.menusetting.addAction(self.actionsetting)
        self.menusetting.addAction(self.actionproxy)
        self.menuabout.addAction(self.actionabout)
        self.menuabout.addAction(self.actionimg_convert)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u54d4\u5494\u6f2b\u753b", None))
        self.actionsetting.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.actionabout.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.actionimg_convert.setText(QCoreApplication.translate("MainWindow", u"waifu2x", None))
        self.actionproxy.setText(QCoreApplication.translate("MainWindow", u"\u4ee3\u7406", None))
        self.menusetting.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.menuabout.setTitle(QCoreApplication.translate("MainWindow", u"\u5de5\u5177", None))
    # retranslateUi

