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


class Ui_Rank(object):
    def setupUi(self, Rank):
        if not Rank.objectName():
            Rank.setObjectName(u"Rank")
        Rank.resize(400, 300)
        self.gridLayout_2 = QGridLayout(Rank)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget = QTabWidget(Rank)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.h24Layout = QGridLayout(self.tab)
        self.h24Layout.setObjectName(u"h24Layout")
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.d7Layout = QGridLayout(self.tab_3)
        self.d7Layout.setObjectName(u"d7Layout")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.d30Layout = QGridLayout(self.tab_2)
        self.d30Layout.setObjectName(u"d30Layout")
        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.retranslateUi(Rank)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Rank)
    # setupUi

    def retranslateUi(self, Rank):
        Rank.setWindowTitle(QCoreApplication.translate("Rank", u"Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Rank", u"24\u5c0f\u65f6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Rank", u"7\u65e5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Rank", u"30\u65e5", None))
    # retranslateUi

