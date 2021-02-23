# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Test(object):
    def setupUi(self, Test):
        if not Test.objectName():
            Test.setObjectName(u"Test")
        Test.resize(400, 286)
        Test.setAcceptDrops(False)
        self.gridLayout = QGridLayout(Test)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = QGraphicsView(Test)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)


        self.retranslateUi(Test)

        QMetaObject.connectSlotsByName(Test)
    # setupUi

    def retranslateUi(self, Test):
        Test.setWindowTitle(QCoreApplication.translate("Test", u"Form", None))
    # retranslateUi

