# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'category.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .qtlistwidget import QtBookList


class Ui_category(object):
    def setupUi(self, category):
        if not category.objectName():
            category.setObjectName(u"category")
        category.resize(400, 300)
        self.gridLayout_2 = QGridLayout(category)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.bookList = QtBookList(category)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.gridLayout_2.addWidget(self.bookList, 0, 0, 1, 1)


        self.retranslateUi(category)

        QMetaObject.connectSlotsByName(category)
    # setupUi

    def retranslateUi(self, category):
        category.setWindowTitle(QCoreApplication.translate("category", u"Form", None))
    # retranslateUi

