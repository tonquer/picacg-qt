# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'download.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_download(object):
    def setupUi(self, download):
        if not download.objectName():
            download.setObjectName(u"download")
        download.resize(608, 372)
        self.gridLayout_2 = QGridLayout(download)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(download)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(download)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(download)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_4 = QPushButton(download)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout.addWidget(self.pushButton_4)

        self.radioButton = QRadioButton(download)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setEnabled(True)
        self.radioButton.setChecked(True)

        self.horizontalLayout.addWidget(self.radioButton)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.tableWidget = QTableWidget(download)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout.addWidget(self.tableWidget, 5, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(download)
        self.pushButton.clicked.connect(download.StartAll)
        self.pushButton_3.clicked.connect(download.StopAll)
        self.pushButton_2.clicked.connect(download.StartConvertAll)
        self.pushButton_4.clicked.connect(download.StopConvertAll)
        self.radioButton.clicked.connect(download.SetAutoConvert)

        QMetaObject.connectSlotsByName(download)
    # setupUi

    def retranslateUi(self, download):
        download.setWindowTitle(QCoreApplication.translate("download", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("download", u"\u5168\u90e8\u5f00\u59cb", None))
        self.pushButton_3.setText(QCoreApplication.translate("download", u"\u5168\u90e8\u6682\u505c", None))
        self.pushButton_2.setText(QCoreApplication.translate("download", u"\u5f00\u59cb\u8f6c\u6362", None))
        self.pushButton_4.setText(QCoreApplication.translate("download", u"\u6682\u505c\u8f6c\u6362", None))
        self.radioButton.setText(QCoreApplication.translate("download", u"\u4e0b\u8f7d\u5b8c\u81ea\u52a8\u8f6c\u6362", None))
    # retranslateUi

