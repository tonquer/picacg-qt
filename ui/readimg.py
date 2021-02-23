# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'readimg.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ReadImg(object):
    def setupUi(self, ReadImg):
        if not ReadImg.objectName():
            ReadImg.setObjectName(u"ReadImg")
        ReadImg.resize(223, 786)
        self.gridLayout_2 = QGridLayout(ReadImg)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_5 = QLabel(ReadImg)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"color: #ee2a24")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_5)

        self.label_6 = QLabel(ReadImg)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"color: #ee2a24")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_6)

        self.line_4 = QFrame(ReadImg)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.radioButton = QRadioButton(ReadImg)
        self.buttonGroup = QButtonGroup(ReadImg)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)

        self.verticalLayout.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(ReadImg)
        self.buttonGroup.addButton(self.radioButton_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout.addWidget(self.radioButton_2)

        self.line_3 = QFrame(ReadImg)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.label_4 = QLabel(ReadImg)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"color: #ee2a24")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_4)

        self.resolutionLabel = QLabel(ReadImg)
        self.resolutionLabel.setObjectName(u"resolutionLabel")

        self.verticalLayout.addWidget(self.resolutionLabel)

        self.sizeLabel = QLabel(ReadImg)
        self.sizeLabel.setObjectName(u"sizeLabel")

        self.verticalLayout.addWidget(self.sizeLabel)

        self.stateLable = QLabel(ReadImg)
        self.stateLable.setObjectName(u"stateLable")

        self.verticalLayout.addWidget(self.stateLable)

        self.epsLabel = QLabel(ReadImg)
        self.epsLabel.setObjectName(u"epsLabel")
        self.epsLabel.setMinimumSize(QSize(0, 20))
        self.epsLabel.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.epsLabel)

        self.progressBar = QProgressBar(ReadImg)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.line = QFrame(ReadImg)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label = QLabel(ReadImg)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color: #ee2a24")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.checkBox = QCheckBox(ReadImg)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.verticalLayout.addWidget(self.checkBox)

        self.label_2 = QLabel(ReadImg)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(ReadImg)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.label_9 = QLabel(ReadImg)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout.addWidget(self.label_9)

        self.resolutionWaifu = QLabel(ReadImg)
        self.resolutionWaifu.setObjectName(u"resolutionWaifu")

        self.verticalLayout.addWidget(self.resolutionWaifu)

        self.sizeWaifu = QLabel(ReadImg)
        self.sizeWaifu.setObjectName(u"sizeWaifu")

        self.verticalLayout.addWidget(self.sizeWaifu)

        self.tickLabel = QLabel(ReadImg)
        self.tickLabel.setObjectName(u"tickLabel")

        self.verticalLayout.addWidget(self.tickLabel)

        self.stateWaifu = QLabel(ReadImg)
        self.stateWaifu.setObjectName(u"stateWaifu")

        self.verticalLayout.addWidget(self.stateWaifu)

        self.line_2 = QFrame(ReadImg)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.lastPage = QPushButton(ReadImg)
        self.lastPage.setObjectName(u"lastPage")
        self.lastPage.setMinimumSize(QSize(0, 0))
        self.lastPage.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.lastPage)

        self.nextPage = QPushButton(ReadImg)
        self.nextPage.setObjectName(u"nextPage")
        self.nextPage.setMinimumSize(QSize(0, 0))
        self.nextPage.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.nextPage)

        self.copyButton = QPushButton(ReadImg)
        self.copyButton.setObjectName(u"copyButton")

        self.verticalLayout.addWidget(self.copyButton)

        self.returePage = QPushButton(ReadImg)
        self.returePage.setObjectName(u"returePage")
        self.returePage.setMinimumSize(QSize(0, 0))
        self.returePage.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.returePage)

        self.pushButton_2 = QPushButton(ReadImg)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        QWidget.setTabOrder(self.radioButton, self.radioButton_2)

        self.retranslateUi(ReadImg)
        self.lastPage.clicked.connect(ReadImg.LastPage)
        self.nextPage.clicked.connect(ReadImg.NextPage)
        self.returePage.clicked.connect(ReadImg.ReturnPage)
        self.radioButton_2.clicked.connect(ReadImg.SwitchPicture)
        self.radioButton.clicked.connect(ReadImg.SwitchPicture)
        self.pushButton_2.clicked.connect(ReadImg.hide)
        self.checkBox.clicked.connect(ReadImg.OpenWaifu)
        self.copyButton.clicked.connect(ReadImg.CopyPicture)

        QMetaObject.connectSlotsByName(ReadImg)
    # setupUi

    def retranslateUi(self, ReadImg):
        ReadImg.setWindowTitle(QCoreApplication.translate("ReadImg", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("ReadImg", u"\u70b9\u51fb\u53f3\u952e\u6253\u5f00\u5173\u95ed", None))
        self.label_6.setText(QCoreApplication.translate("ReadImg", u"\u6309\u4f4f\u5de6Alt+\u6eda\u8f6e\u653e\u5927", None))
        self.radioButton.setText(QCoreApplication.translate("ReadImg", u"\u94fa\u6ee1\u9ad8\u5ea6\uff08\u8fd8\u539f\u56fe\u7247\uff09", None))
        self.radioButton_2.setText(QCoreApplication.translate("ReadImg", u"\u94fa\u6ee1\u5bbd\u5ea6\uff08\u8fd8\u539f\u56fe\u7247\uff09", None))
        self.label_4.setText(QCoreApplication.translate("ReadImg", u"\u56fe\u7247\u4fe1\u606f", None))
        self.resolutionLabel.setText(QCoreApplication.translate("ReadImg", u"\u5206\u8fa8\u7387\uff1a", None))
        self.sizeLabel.setText(QCoreApplication.translate("ReadImg", u"\u5927\u5c0f\uff1a", None))
        self.stateLable.setText(QCoreApplication.translate("ReadImg", u"\u72b6\u6001\uff1a", None))
        self.epsLabel.setText(QCoreApplication.translate("ReadImg", u"\u4f4d\u7f6e\uff1a", None))
        self.label.setText(QCoreApplication.translate("ReadImg", u"Waifu2x\u53c2\u6570", None))
        self.checkBox.setText(QCoreApplication.translate("ReadImg", u"\u6253\u5f00Waifu2x", None))
        self.label_2.setText(QCoreApplication.translate("ReadImg", u"\u566a\u70b9\u7b49\u7ea7\uff1a3", None))
        self.label_3.setText(QCoreApplication.translate("ReadImg", u"\u653e\u5927\u500d\u6570\uff1a2", None))
        self.label_9.setText(QCoreApplication.translate("ReadImg", u"\u8f6c\u7801\u6a21\u5f0f\uff1aGPU", None))
        self.resolutionWaifu.setText(QCoreApplication.translate("ReadImg", u"\u5206\u8fa8\u7387\uff1a", None))
        self.sizeWaifu.setText(QCoreApplication.translate("ReadImg", u"\u5927\u5c0f\uff1a", None))
        self.tickLabel.setText(QCoreApplication.translate("ReadImg", u"\u8017\u65f6\uff1a", None))
        self.stateWaifu.setText(QCoreApplication.translate("ReadImg", u"\u72b6\u6001\uff1a", None))
        self.lastPage.setText(QCoreApplication.translate("ReadImg", u"\u4e0a\u4e00\u9875", None))
        self.nextPage.setText(QCoreApplication.translate("ReadImg", u"\u4e0b\u4e00\u9875", None))
        self.copyButton.setText(QCoreApplication.translate("ReadImg", u"\u590d\u5236\u56fe\u7247", None))
        self.returePage.setText(QCoreApplication.translate("ReadImg", u"\u8fd4\u56de", None))
        self.pushButton_2.setText(QCoreApplication.translate("ReadImg", u"\u9690\u85cf", None))
    # retranslateUi

