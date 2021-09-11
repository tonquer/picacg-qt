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
        ReadImg.resize(299, 730)
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
        self.resolutionLabel.setStyleSheet(u"")

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

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.resolutionWaifu = QLabel(ReadImg)
        self.resolutionWaifu.setObjectName(u"resolutionWaifu")

        self.gridLayout.addWidget(self.resolutionWaifu, 5, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.noiseLabel = QLabel(ReadImg)
        self.noiseLabel.setObjectName(u"noiseLabel")

        self.horizontalLayout_3.addWidget(self.noiseLabel)

        self.noiseBox = QComboBox(ReadImg)
        self.noiseBox.addItem("")
        self.noiseBox.addItem("")
        self.noiseBox.addItem("")
        self.noiseBox.addItem("")
        self.noiseBox.addItem("")
        self.noiseBox.setObjectName(u"noiseBox")

        self.horizontalLayout_3.addWidget(self.noiseBox)


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)

        self.checkBox = QCheckBox(ReadImg)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setStyleSheet(u"")
        self.checkBox.setChecked(True)

        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)

        self.sizeWaifu = QLabel(ReadImg)
        self.sizeWaifu.setObjectName(u"sizeWaifu")

        self.gridLayout.addWidget(self.sizeWaifu, 6, 0, 1, 1)

        self.label_8 = QLabel(ReadImg)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(35, 16777215))

        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)

        self.label_3 = QLabel(ReadImg)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.stateWaifu = QLabel(ReadImg)
        self.stateWaifu.setObjectName(u"stateWaifu")

        self.gridLayout.addWidget(self.stateWaifu, 8, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.scaleLabel = QLabel(ReadImg)
        self.scaleLabel.setObjectName(u"scaleLabel")

        self.horizontalLayout_6.addWidget(self.scaleLabel)

        self.scaleBox = QDoubleSpinBox(ReadImg)
        self.scaleBox.setObjectName(u"scaleBox")
        self.scaleBox.setDecimals(1)
        self.scaleBox.setMaximum(32.000000000000000)
        self.scaleBox.setSingleStep(0.100000000000000)
        self.scaleBox.setValue(2.000000000000000)

        self.horizontalLayout_6.addWidget(self.scaleBox)


        self.gridLayout.addLayout(self.horizontalLayout_6, 2, 1, 1, 1)

        self.label_2 = QLabel(ReadImg)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.tickLabel = QLabel(ReadImg)
        self.tickLabel.setObjectName(u"tickLabel")

        self.gridLayout.addWidget(self.tickLabel, 7, 0, 1, 1)

        self.label_9 = QLabel(ReadImg)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.modelLabel = QLabel(ReadImg)
        self.modelLabel.setObjectName(u"modelLabel")

        self.horizontalLayout_8.addWidget(self.modelLabel)

        self.modelBox = QComboBox(ReadImg)
        self.modelBox.addItem("")
        self.modelBox.addItem("")
        self.modelBox.addItem("")
        self.modelBox.addItem("")
        self.modelBox.setObjectName(u"modelBox")

        self.horizontalLayout_8.addWidget(self.modelBox)


        self.gridLayout.addLayout(self.horizontalLayout_8, 3, 1, 1, 1)

        self.gpuLabel = QLabel(ReadImg)
        self.gpuLabel.setObjectName(u"gpuLabel")

        self.gridLayout.addWidget(self.gpuLabel, 4, 1, 1, 1)

        self.waifu2xRes = QLabel(ReadImg)
        self.waifu2xRes.setObjectName(u"waifu2xRes")

        self.gridLayout.addWidget(self.waifu2xRes, 5, 1, 1, 1)

        self.waifu2xSize = QLabel(ReadImg)
        self.waifu2xSize.setObjectName(u"waifu2xSize")

        self.gridLayout.addWidget(self.waifu2xSize, 6, 1, 1, 1)

        self.waifu2xTick = QLabel(ReadImg)
        self.waifu2xTick.setObjectName(u"waifu2xTick")

        self.gridLayout.addWidget(self.waifu2xTick, 7, 1, 1, 1)

        self.waifu2xStatus = QLabel(ReadImg)
        self.waifu2xStatus.setObjectName(u"waifu2xStatus")

        self.gridLayout.addWidget(self.waifu2xStatus, 8, 1, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.waifu2xSave = QPushButton(ReadImg)
        self.waifu2xSave.setObjectName(u"waifu2xSave")

        self.horizontalLayout_9.addWidget(self.waifu2xSave)

        self.waifu2xCancle = QPushButton(ReadImg)
        self.waifu2xCancle.setObjectName(u"waifu2xCancle")

        self.horizontalLayout_9.addWidget(self.waifu2xCancle)


        self.gridLayout.addLayout(self.horizontalLayout_9, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.line_2 = QFrame(ReadImg)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label_6 = QLabel(ReadImg)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"color: #ee2a24")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_6)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_5 = QLabel(ReadImg)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(90, 16777215))
        self.label_5.setStyleSheet(u"")
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_5)

        self.comboBox = QComboBox(ReadImg)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_11.addWidget(self.comboBox)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.zoomLabel = QLabel(ReadImg)
        self.zoomLabel.setObjectName(u"zoomLabel")

        self.horizontalLayout_10.addWidget(self.zoomLabel)

        self.zoomSlider = QSlider(ReadImg)
        self.zoomSlider.setObjectName(u"zoomSlider")
        self.zoomSlider.setStyleSheet(u"")
        self.zoomSlider.setMinimum(10)
        self.zoomSlider.setMaximum(200)
        self.zoomSlider.setSingleStep(10)
        self.zoomSlider.setValue(120)
        self.zoomSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_10.addWidget(self.zoomSlider)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.line_3 = QFrame(ReadImg)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.copyButton = QPushButton(ReadImg)
        self.copyButton.setObjectName(u"copyButton")
        self.copyButton.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.copyButton)

        self.pushButton_2 = QPushButton(ReadImg)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.fullButton = QPushButton(ReadImg)
        self.fullButton.setObjectName(u"fullButton")

        self.verticalLayout.addWidget(self.fullButton)

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
        self.lastPage.clicked.connect(ReadImg.LastPage)
        self.copyButton.clicked.connect(ReadImg.CopyPicture)
        self.nextPage.clicked.connect(ReadImg.NextPage)
        self.pushButton_4.clicked.connect(ReadImg.OpenLastEps)
        self.pushButton_2.clicked.connect(ReadImg.hide)
        self.returePage.clicked.connect(ReadImg.ReturnPage)
        self.checkBox.clicked.connect(ReadImg.OpenWaifu)
        self.fullButton.clicked.connect(ReadImg.FullScreen)
        self.waifu2xSave.clicked.connect(ReadImg.Waifu2xSave)
        self.waifu2xCancle.clicked.connect(ReadImg.Waifu2xCancle)
        self.zoomSlider.valueChanged.connect(ReadImg.ScalePicture)
        self.comboBox.currentIndexChanged.connect(ReadImg.ChangeReadMode)

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
        self.resolutionWaifu.setText(QCoreApplication.translate("ReadImg", u"\u5206\u8fa8\u7387\uff1a", None))
        self.noiseLabel.setText(QCoreApplication.translate("ReadImg", u"3", None))
        self.noiseBox.setItemText(0, QCoreApplication.translate("ReadImg", u"\u81ea\u52a8", None))
        self.noiseBox.setItemText(1, QCoreApplication.translate("ReadImg", u"0", None))
        self.noiseBox.setItemText(2, QCoreApplication.translate("ReadImg", u"1", None))
        self.noiseBox.setItemText(3, QCoreApplication.translate("ReadImg", u"2", None))
        self.noiseBox.setItemText(4, QCoreApplication.translate("ReadImg", u"3", None))

        self.checkBox.setText(QCoreApplication.translate("ReadImg", u"\u6253\u5f00Waifu2x", None))
        self.sizeWaifu.setText(QCoreApplication.translate("ReadImg", u"\u5927\u5c0f\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("ReadImg", u"\u6a21\u578b\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("ReadImg", u"\u653e\u5927\u500d\u6570\uff1a", None))
        self.stateWaifu.setText(QCoreApplication.translate("ReadImg", u"\u72b6\u6001\uff1a", None))
        self.scaleLabel.setText(QCoreApplication.translate("ReadImg", u"2", None))
        self.label_2.setText(QCoreApplication.translate("ReadImg", u"\u53bb\u566a\u7b49\u7ea7\uff1a", None))
        self.tickLabel.setText(QCoreApplication.translate("ReadImg", u"\u8017\u65f6\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("ReadImg", u"\u8f6c\u6362\u6a21\u5f0f\uff1a", None))
        self.modelLabel.setText(QCoreApplication.translate("ReadImg", u"CUNET", None))
        self.modelBox.setItemText(0, QCoreApplication.translate("ReadImg", u"\u81ea\u52a8", None))
        self.modelBox.setItemText(1, QCoreApplication.translate("ReadImg", u"cunet", None))
        self.modelBox.setItemText(2, QCoreApplication.translate("ReadImg", u"photo", None))
        self.modelBox.setItemText(3, QCoreApplication.translate("ReadImg", u"anime_style_art_rgb", None))

        self.gpuLabel.setText(QCoreApplication.translate("ReadImg", u"GPU", None))
        self.waifu2xRes.setText("")
        self.waifu2xSize.setText("")
        self.waifu2xTick.setText("")
        self.waifu2xStatus.setText("")
        self.waifu2xSave.setText(QCoreApplication.translate("ReadImg", u"\u4fee\u6539", None))
        self.waifu2xCancle.setText(QCoreApplication.translate("ReadImg", u"\u4fdd\u5b58", None))
        self.label_6.setText(QCoreApplication.translate("ReadImg", u"\u7ffb\u9875\u8bbe\u7f6e", None))
        self.label_5.setText(QCoreApplication.translate("ReadImg", u"\u7ffb\u9875\u6a21\u5f0f\uff1a", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("ReadImg", u"\u4e0a\u4e0b\u6eda\u52a8", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("ReadImg", u"\u9ed8\u8ba4", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("ReadImg", u"\u5de6\u53f3\u53cc\u9875", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("ReadImg", u"\u53f3\u5de6\u53cc\u9875", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("ReadImg", u"\u5de6\u53f3\u6eda\u52a8", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("ReadImg", u"\u53f3\u5de6\u6eda\u52a8", None))

        self.zoomLabel.setText(QCoreApplication.translate("ReadImg", u"\u7f29\u653e\uff08120%\uff09", None))
        self.copyButton.setText(QCoreApplication.translate("ReadImg", u"\u6253\u5f00\u56fe\u7247\u5de5\u5177", None))
        self.pushButton_2.setText(QCoreApplication.translate("ReadImg", u"\u9690\u85cf", None))
        self.fullButton.setText(QCoreApplication.translate("ReadImg", u"\u5168\u5c4f", None))
        self.returePage.setText(QCoreApplication.translate("ReadImg", u"\u8fd4\u56de", None))
        self.pushButton_4.setText(QCoreApplication.translate("ReadImg", u"\u4e0a\u4e00\u7ae0", None))
        self.pushButton_5.setText(QCoreApplication.translate("ReadImg", u"\u4e0b\u4e00\u7ae0", None))
        self.lastPage.setText(QCoreApplication.translate("ReadImg", u"\u4e0a\u4e00\u9875", None))
        self.nextPage.setText(QCoreApplication.translate("ReadImg", u"\u4e0b\u4e00\u9875", None))
    # retranslateUi

