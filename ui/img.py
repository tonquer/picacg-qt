# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'img.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Img(object):
    def setupUi(self, Img):
        if not Img.objectName():
            Img.setObjectName(u"Img")
        Img.resize(417, 351)
        self.gridLayout = QGridLayout(Img)
        self.gridLayout.setObjectName(u"gridLayout")
        self.graphicsView = QGraphicsView(Img)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.oepnButton = QPushButton(Img)
        self.oepnButton.setObjectName(u"oepnButton")

        self.verticalLayout_3.addWidget(self.oepnButton)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_3 = QPushButton(Img)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton = QPushButton(Img)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.saveButton = QPushButton(Img)
        self.saveButton.setObjectName(u"saveButton")

        self.verticalLayout_3.addWidget(self.saveButton)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radioButton = QRadioButton(Img)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout_2.addWidget(self.radioButton)

        self.comboBox = QComboBox(Img)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_2.addWidget(self.comboBox)

        self.changeButton = QPushButton(Img)
        self.changeButton.setObjectName(u"changeButton")

        self.verticalLayout_2.addWidget(self.changeButton)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)


        self.retranslateUi(Img)
        self.changeButton.clicked.connect(Img.StartWaifu2x)
        self.saveButton.clicked.connect(Img.SavePicture)
        self.pushButton_3.clicked.connect(Img.ReduceScalePic)
        self.pushButton.clicked.connect(Img.AddScalePic)
        self.oepnButton.clicked.connect(Img.OpenPicture)
        self.radioButton.clicked.connect(Img.SwithPicture)
        self.comboBox.currentIndexChanged.connect(Img.ChangeModel)

        QMetaObject.connectSlotsByName(Img)
    # setupUi

    def retranslateUi(self, Img):
        Img.setWindowTitle(QCoreApplication.translate("Img", u"Form", None))
        self.oepnButton.setText(QCoreApplication.translate("Img", u"\u6253\u5f00\u56fe\u7247", None))
        self.pushButton_3.setText(QCoreApplication.translate("Img", u"\u7f29\u5c0f", None))
        self.pushButton.setText(QCoreApplication.translate("Img", u"\u653e\u5927", None))
        self.saveButton.setText(QCoreApplication.translate("Img", u"\u4fdd\u5b58\u56fe\u7247", None))
        self.radioButton.setText(QCoreApplication.translate("Img", u"waifu2x", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Img", u"cunet(\u4e0d\u653e\u5927)", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Img", u"cunet", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Img", u"photo", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Img", u"anime_style_art_rgb", None))

        self.changeButton.setText(QCoreApplication.translate("Img", u"\u8f6c\u6362", None))
    # retranslateUi

