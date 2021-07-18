# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'index.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .qtlistwidget import QtBookList


class Ui_Index(object):
    def setupUi(self, Index):
        if not Index.objectName():
            Index.setObjectName(u"Index")
        Index.resize(1125, 808)
        self.verticalLayout_3 = QVBoxLayout(Index)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tabWidget = QTabWidget(Index)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"QTabWidget:pane {border-top:0px solid #e8f3f9;background:  transparent; }")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.randomList = QtBookList(self.tab)
        self.randomList.setObjectName(u"randomList")
        self.randomList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.verticalLayout_2.addWidget(self.randomList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(1080, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.refreshButton = QPushButton(self.tab)
        self.refreshButton.setObjectName(u"refreshButton")

        self.horizontalLayout.addWidget(self.refreshButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout = QVBoxLayout(self.tab_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.godList = QtBookList(self.tab_2)
        self.godList.setObjectName(u"godList")
        self.godList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.verticalLayout.addWidget(self.godList)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.magicList = QtBookList(self.tab_3)
        self.magicList.setObjectName(u"magicList")
        self.magicList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.verticalLayout_4.addWidget(self.magicList)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_3.addWidget(self.tabWidget)


        self.retranslateUi(Index)
        self.refreshButton.clicked.connect(Index.InitRandom)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Index)
    # setupUi

    def retranslateUi(self, Index):
        Index.setWindowTitle(QCoreApplication.translate("Index", u"Form", None))
        self.refreshButton.setText(QCoreApplication.translate("Index", u"\u5237\u65b0\uff08F5\uff09", None))
#if QT_CONFIG(shortcut)
        self.refreshButton.setShortcut(QCoreApplication.translate("Index", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Index", u"\u968f\u673a\u672c\u5b50", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Index", u"\u54d4\u5494\u795e\u63a8\u8350", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Index", u"\u54d4\u5494\u9b54\u63a8\u8350", None))
    # retranslateUi

