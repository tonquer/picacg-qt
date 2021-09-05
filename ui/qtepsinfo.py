# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qtepsinfo.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_EpsInfo(object):
    def setupUi(self, EpsInfo):
        if not EpsInfo.objectName():
            EpsInfo.setObjectName(u"EpsInfo")
        EpsInfo.resize(526, 82)
        self.gridLayout_2 = QGridLayout(EpsInfo)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(EpsInfo)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.pushButton = QPushButton(EpsInfo)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(EpsInfo)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(EpsInfo)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(EpsInfo)
        self.pushButton.clicked.connect(EpsInfo.SelectAll)
        self.pushButton_2.clicked.connect(EpsInfo.CancleSelect)
        self.pushButton_3.clicked.connect(EpsInfo.StartDownload)

        QMetaObject.connectSlotsByName(EpsInfo)
    # setupUi

    def retranslateUi(self, EpsInfo):
        EpsInfo.setWindowTitle(QCoreApplication.translate("EpsInfo", u"\u7ae0\u8282\u5217\u8868", None))
        self.label.setText(QCoreApplication.translate("EpsInfo", u"\u7ae0\u8282", None))
        self.pushButton.setText(QCoreApplication.translate("EpsInfo", u"\u5168\u9009", None))
        self.pushButton_2.setText(QCoreApplication.translate("EpsInfo", u"\u53cd\u9009", None))
        self.pushButton_3.setText(QCoreApplication.translate("EpsInfo", u"\u4e0b\u8f7d", None))
    # retranslateUi

