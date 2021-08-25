# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rank.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .qtlistwidget import QtBookList


class Ui_Rank(object):
    def setupUi(self, Rank):
        if not Rank.objectName():
            Rank.setObjectName(u"Rank")
        Rank.resize(400, 300)
        self.gridLayout_2 = QGridLayout(Rank)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget = QTabWidget(Rank)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"QTabWidget:pane {border-top:0px solid #e8f3f9;background:  transparent; }")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setStyleSheet(u"")
        self.h24Layout = QGridLayout(self.tab)
        self.h24Layout.setObjectName(u"h24Layout")
        self.h24BookList = QtBookList(self.tab)
        self.h24BookList.setObjectName(u"h24BookList")
        self.h24BookList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.h24Layout.addWidget(self.h24BookList, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.d7Layout = QGridLayout(self.tab_3)
        self.d7Layout.setObjectName(u"d7Layout")
        self.d7BookList = QtBookList(self.tab_3)
        self.d7BookList.setObjectName(u"d7BookList")
        self.d7BookList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.d7Layout.addWidget(self.d7BookList, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.d30Layout = QGridLayout(self.tab_2)
        self.d30Layout.setObjectName(u"d30Layout")
        self.d30BookList = QtBookList(self.tab_2)
        self.d30BookList.setObjectName(u"d30BookList")
        self.d30BookList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.d30Layout.addWidget(self.d30BookList, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout = QGridLayout(self.tab_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.kindList = QtBookList(self.tab_4)
        self.kindList.setObjectName(u"kindList")
        self.kindList.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
"QListWidget::item { border-bottom: 1px solid black; }")

        self.gridLayout.addWidget(self.kindList, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_4, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.retranslateUi(Rank)
        self.tabWidget.currentChanged.connect(Rank.SwitchPage)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Rank)
    # setupUi

    def retranslateUi(self, Rank):
        Rank.setWindowTitle(QCoreApplication.translate("Rank", u"Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Rank", u"24\u5c0f\u65f6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Rank", u"7\u65e5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Rank", u"30\u65e5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Rank", u"\u9a91\u58eb\u699c", None))
    # retranslateUi

