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
        ReadImg.resize(207, 647)
        ReadImg.setAutoFillBackground(False)
        ReadImg.setStyleSheet(u"")
        self.gridLayout_2 = QGridLayout(ReadImg)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.line_6 = QFrame(ReadImg)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_6)

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
        self.checkBox.setStyleSheet(u"")
        self.checkBox.setChecked(True)

        self.verticalLayout.addWidget(self.checkBox)

        self.label_2 = QLabel(ReadImg)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(ReadImg)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_8 = QLabel(ReadImg)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(35, 16777215))

        self.horizontalLayout_6.addWidget(self.label_8)

        self.modelBox = QComboBox(ReadImg)
        self.modelBox.addItem("")
        self.modelBox.addItem("")
        self.modelBox.addItem("")
        self.modelBox.addItem("")
        self.modelBox.setObjectName(u"modelBox")

        self.horizontalLayout_6.addWidget(self.modelBox)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

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

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radioButton = QRadioButton(ReadImg)
        self.buttonGroup = QButtonGroup(ReadImg)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)

        self.horizontalLayout_4.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(ReadImg)
        self.buttonGroup.addButton(self.radioButton_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_4.addWidget(self.radioButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.copyButton = QPushButton(ReadImg)
        self.copyButton.setObjectName(u"copyButton")

        self.verticalLayout.addWidget(self.copyButton)

        self.pushButton_2 = QPushButton(ReadImg)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.returePage = QPushButton(ReadImg)
        self.returePage.setObjectName(u"returePage")
        self.returePage.setMinimumSize(QSize(0, 0))
        self.returePage.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.returePage)

        self.line_5 = QFrame(ReadImg)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")

        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_4 = QPushButton(ReadImg)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_5.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(ReadImg)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_5.addWidget(self.pushButton_5)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.line_7 = QFrame(ReadImg)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lastPage = QPushButton(ReadImg)
        self.lastPage.setObjectName(u"lastPage")
        self.lastPage.setMinimumSize(QSize(0, 0))
        self.lastPage.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.lastPage)

        self.nextPage = QPushButton(ReadImg)
        self.nextPage.setObjectName(u"nextPage")
        self.nextPage.setMinimumSize(QSize(0, 0))
        self.nextPage.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.nextPage)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line_4 = QFrame(ReadImg)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)


        self.retranslateUi(ReadImg)
        self.pushButton_5.clicked.connect(ReadImg.OpenNextEps)
        self.modelBox.currentIndexChanged.connect(ReadImg.SwitchModel)
        self.lastPage.clicked.connect(ReadImg.LastPage)
        self.radioButton.clicked.connect(ReadImg.SwitchPicture)
        self.radioButton_2.clicked.connect(ReadImg.SwitchPicture)
        self.copyButton.clicked.connect(ReadImg.CopyPicture)
        self.nextPage.clicked.connect(ReadImg.NextPage)
        self.pushButton_4.clicked.connect(ReadImg.OpenLastEps)
        self.pushButton_2.clicked.connect(ReadImg.hide)
        self.returePage.clicked.connect(ReadImg.ReturnPage)
        self.checkBox.clicked.connect(ReadImg.OpenWaifu)

        QMetaObject.connectSlotsByName(ReadImg)
    # setupUi

    def retranslateUi(self, ReadImg):
        ReadImg.setWindowTitle(QCoreApplication.translate("ReadImg", u"Form", None))
        self.label_4.setText(QCoreApplication.translate("ReadImg", u"\u56fe\u7247\u4fe1\u606f", None))
        self.resolutionLabel.setText(QCoreApplication.translate("ReadImg", u"\u5206\u8fa8\u7387\uff1a", None))
        self.sizeLabel.setText(QCoreApplication.translate("ReadImg", u"\u5927\u5c0f\uff1a", None))
        self.stateLable.setText(QCoreApplication.translate("ReadImg", u"\u72b6\u6001\uff1a", None))
        self.epsLabel.setText(QCoreApplication.translate("ReadImg", u"\u4f4d\u7f6e\uff1a", None))
        self.label.setText(QCoreApplication.translate("ReadImg", u"Waifu2x\u53c2\u6570", None))
        self.checkBox.setText(QCoreApplication.translate("ReadImg", u"\u6253\u5f00Waifu2x", None))
        self.label_2.setText(QCoreApplication.translate("ReadImg", u"\u566a\u70b9\u7b49\u7ea7\uff1a3", None))
        self.label_3.setText(QCoreApplication.translate("ReadImg", u"\u653e\u5927\u500d\u6570\uff1a2", None))
        self.label_8.setText(QCoreApplication.translate("ReadImg", u"\u6a21\u578b\uff1a", None))
        self.modelBox.setItemText(0, QCoreApplication.translate("ReadImg", u"cunet\uff08\u4e0d\u653e\u5927\uff09", None))
        self.modelBox.setItemText(1, QCoreApplication.translate("ReadImg", u"cunet", None))
        self.modelBox.setItemText(2, QCoreApplication.translate("ReadImg", u"photo", None))
        self.modelBox.setItemText(3, QCoreApplication.translate("ReadImg", u"anime_style_art_rgb", None))

        self.label_9.setText(QCoreApplication.translate("ReadImg", u"\u8f6c\u7801\u6a21\u5f0f\uff1aGPU", None))
        self.resolutionWaifu.setText(QCoreApplication.translate("ReadImg", u"\u5206\u8fa8\u7387\uff1a", None))
        self.sizeWaifu.setText(QCoreApplication.translate("ReadImg", u"\u5927\u5c0f\uff1a", None))
        self.tickLabel.setText(QCoreApplication.translate("ReadImg", u"\u8017\u65f6\uff1a", None))
        self.stateWaifu.setText(QCoreApplication.translate("ReadImg", u"\u72b6\u6001\uff1a", None))
        self.radioButton.setText(QCoreApplication.translate("ReadImg", u"\u94fa\u6ee1\u9ad8\u5ea6", None))
        self.radioButton_2.setText(QCoreApplication.translate("ReadImg", u"\u94fa\u6ee1\u5bbd\u5ea6", None))
        self.copyButton.setText(QCoreApplication.translate("ReadImg", u"\u6253\u5f00\u56fe\u7247\u5de5\u5177", None))
        self.pushButton_2.setText(QCoreApplication.translate("ReadImg", u"\u9690\u85cf", None))
        self.returePage.setText(QCoreApplication.translate("ReadImg", u"\u8fd4\u56de", None))
        self.pushButton_4.setText(QCoreApplication.translate("ReadImg", u"\u4e0a\u4e00\u7ae0", None))
        self.pushButton_5.setText(QCoreApplication.translate("ReadImg", u"\u4e0b\u4e00\u7ae0", None))
        self.lastPage.setText(QCoreApplication.translate("ReadImg", u"\u4e0a\u4e00\u9875", None))
        self.nextPage.setText(QCoreApplication.translate("ReadImg", u"\u4e0b\u4e00\u9875", None))
    # retranslateUi

