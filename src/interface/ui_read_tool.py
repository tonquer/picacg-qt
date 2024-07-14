# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_read_tool.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from component.box.wheel_combo_box import WheelComboBox
from component.box.wheel_double_spin_box import WheelDoubleSpinBox
from component.box.wheel_slider import WheelSlider
from component.box.wheel_spin_box import WheelSpinBox
from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_ReadImg(object):
    def setupUi(self, ReadImg):
        if not ReadImg.objectName():
            ReadImg.setObjectName(u"ReadImg")
        ReadImg.resize(328, 825)
        ReadImg.setAutoFillBackground(False)
        ReadImg.setStyleSheet(u"")
        self.gridLayout_2 = QGridLayout(ReadImg)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.scrollArea22 = SmoothScrollArea(ReadImg)
        self.scrollArea22.setObjectName(u"scrollArea22")
        self.scrollArea22.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 309, 827))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.line_6 = QFrame(self.scrollAreaWidgetContents)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_6)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"color: #ee2a24")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_4)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.epsLabel = QLabel(self.scrollAreaWidgetContents)
        self.epsLabel.setObjectName(u"epsLabel")
        self.epsLabel.setMinimumSize(QSize(0, 20))
        self.epsLabel.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_3.addWidget(self.epsLabel, 2, 0, 1, 1)

        self.stateLable = QLabel(self.scrollAreaWidgetContents)
        self.stateLable.setObjectName(u"stateLable")

        self.gridLayout_3.addWidget(self.stateLable, 1, 0, 1, 1)

        self.sizeLabel = QLabel(self.scrollAreaWidgetContents)
        self.sizeLabel.setObjectName(u"sizeLabel")

        self.gridLayout_3.addWidget(self.sizeLabel, 0, 0, 1, 1)

        self.resolutionLabel = QLabel(self.scrollAreaWidgetContents)
        self.resolutionLabel.setObjectName(u"resolutionLabel")
        self.resolutionLabel.setMaximumSize(QSize(40, 16777215))
        self.resolutionLabel.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.resolutionLabel, 3, 0, 1, 1)

        self.sizeLabel2 = QLabel(self.scrollAreaWidgetContents)
        self.sizeLabel2.setObjectName(u"sizeLabel2")

        self.gridLayout_3.addWidget(self.sizeLabel2, 0, 1, 1, 1)

        self.stateLable2 = QLabel(self.scrollAreaWidgetContents)
        self.stateLable2.setObjectName(u"stateLable2")

        self.gridLayout_3.addWidget(self.stateLable2, 1, 1, 1, 1)

        self.epsLabel2 = QLabel(self.scrollAreaWidgetContents)
        self.epsLabel2.setObjectName(u"epsLabel2")

        self.gridLayout_3.addWidget(self.epsLabel2, 2, 1, 1, 1)

        self.resolutionLabel2 = QLabel(self.scrollAreaWidgetContents)
        self.resolutionLabel2.setObjectName(u"resolutionLabel2")

        self.gridLayout_3.addWidget(self.resolutionLabel2, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color: #ee2a24")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.modelLabel = QLabel(self.scrollAreaWidgetContents)
        self.modelLabel.setObjectName(u"modelLabel")

        self.horizontalLayout_8.addWidget(self.modelLabel)

        self.modelBox = WheelComboBox(self.scrollAreaWidgetContents)
        self.modelBox.addItem("")
        self.modelBox.addItem("")
        self.modelBox.addItem("")
        self.modelBox.addItem("")
        self.modelBox.setObjectName(u"modelBox")

        self.horizontalLayout_8.addWidget(self.modelBox)


        self.gridLayout.addLayout(self.horizontalLayout_8, 6, 1, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(35, 16777215))

        self.gridLayout.addWidget(self.label_8, 6, 0, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 1)

        self.tickLabel = QLabel(self.scrollAreaWidgetContents)
        self.tickLabel.setObjectName(u"tickLabel")

        self.gridLayout.addWidget(self.tickLabel, 10, 0, 1, 1)

        self.waifu2xTick = QLabel(self.scrollAreaWidgetContents)
        self.waifu2xTick.setObjectName(u"waifu2xTick")

        self.gridLayout.addWidget(self.waifu2xTick, 10, 1, 1, 1)

        self.gpuLabel = QLabel(self.scrollAreaWidgetContents)
        self.gpuLabel.setObjectName(u"gpuLabel")

        self.gridLayout.addWidget(self.gpuLabel, 7, 1, 1, 1)

        self.waifu2xRes = QLabel(self.scrollAreaWidgetContents)
        self.waifu2xRes.setObjectName(u"waifu2xRes")

        self.gridLayout.addWidget(self.waifu2xRes, 8, 1, 1, 1)

        self.waifu2xStatus = QLabel(self.scrollAreaWidgetContents)
        self.waifu2xStatus.setObjectName(u"waifu2xStatus")

        self.gridLayout.addWidget(self.waifu2xStatus, 11, 1, 1, 1)

        self.waifu2xSave = QPushButton(self.scrollAreaWidgetContents)
        self.waifu2xSave.setObjectName(u"waifu2xSave")

        self.gridLayout.addWidget(self.waifu2xSave, 3, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.waifu2xCancle = QPushButton(self.scrollAreaWidgetContents)
        self.waifu2xCancle.setObjectName(u"waifu2xCancle")

        self.horizontalLayout_9.addWidget(self.waifu2xCancle)


        self.gridLayout.addLayout(self.horizontalLayout_9, 3, 1, 1, 1)

        self.waifu2xSize = QLabel(self.scrollAreaWidgetContents)
        self.waifu2xSize.setObjectName(u"waifu2xSize")

        self.gridLayout.addWidget(self.waifu2xSize, 9, 1, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)

        self.checkBox = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setStyleSheet(u"")
        self.checkBox.setChecked(True)

        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)

        self.curWaifu2x = QCheckBox(self.scrollAreaWidgetContents)
        self.curWaifu2x.setObjectName(u"curWaifu2x")

        self.gridLayout.addWidget(self.curWaifu2x, 1, 1, 1, 1)

        self.stateWaifu = QLabel(self.scrollAreaWidgetContents)
        self.stateWaifu.setObjectName(u"stateWaifu")

        self.gridLayout.addWidget(self.stateWaifu, 11, 0, 1, 1)

        self.resolutionWaifu = QLabel(self.scrollAreaWidgetContents)
        self.resolutionWaifu.setObjectName(u"resolutionWaifu")

        self.gridLayout.addWidget(self.resolutionWaifu, 8, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.scaleLabel = QLabel(self.scrollAreaWidgetContents)
        self.scaleLabel.setObjectName(u"scaleLabel")

        self.horizontalLayout_6.addWidget(self.scaleLabel)

        self.scaleBox = WheelDoubleSpinBox(self.scrollAreaWidgetContents)
        self.scaleBox.setObjectName(u"scaleBox")
        self.scaleBox.setDecimals(1)
        self.scaleBox.setMaximum(32.000000000000000)
        self.scaleBox.setSingleStep(0.100000000000000)
        self.scaleBox.setValue(2.000000000000000)

        self.horizontalLayout_6.addWidget(self.scaleBox)


        self.gridLayout.addLayout(self.horizontalLayout_6, 5, 1, 1, 1)

        self.sizeWaifu = QLabel(self.scrollAreaWidgetContents)
        self.sizeWaifu.setObjectName(u"sizeWaifu")

        self.gridLayout.addWidget(self.sizeWaifu, 9, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.noiseLabel = QLabel(self.scrollAreaWidgetContents)
        self.noiseLabel.setObjectName(u"noiseLabel")

        self.horizontalLayout_3.addWidget(self.noiseLabel)

        self.noiseBox = WheelComboBox(self.scrollAreaWidgetContents)
        self.noiseBox.addItem("")
        self.noiseBox.addItem("")
        self.noiseBox.addItem("")
        self.noiseBox.addItem("")
        self.noiseBox.addItem("")
        self.noiseBox.setObjectName(u"noiseBox")

        self.horizontalLayout_3.addWidget(self.noiseBox)


        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 1, 1, 1)

        self.preDownWaifu2x = QCheckBox(self.scrollAreaWidgetContents)
        self.preDownWaifu2x.setObjectName(u"preDownWaifu2x")

        self.gridLayout.addWidget(self.preDownWaifu2x, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"color: #ee2a24")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_6)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(90, 16777215))
        self.label_5.setStyleSheet(u"")
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_5)

        self.comboBox = WheelComboBox(self.scrollAreaWidgetContents)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
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
        self.zoomLabel = QLabel(self.scrollAreaWidgetContents)
        self.zoomLabel.setObjectName(u"zoomLabel")

        self.horizontalLayout_10.addWidget(self.zoomLabel)

        self.zoomSlider = WheelSlider(self.scrollAreaWidgetContents)
        self.zoomSlider.setObjectName(u"zoomSlider")
        self.zoomSlider.setStyleSheet(u"")
        self.zoomSlider.setMinimum(10)
        self.zoomSlider.setMaximum(200)
        self.zoomSlider.setSingleStep(10)
        self.zoomSlider.setValue(120)
        self.zoomSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_10.addWidget(self.zoomSlider)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.line_3 = QFrame(self.scrollAreaWidgetContents)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"color: #ee2a24")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_7)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_12.addWidget(self.label_10)

        self.scrollSpeed = WheelSpinBox(self.scrollAreaWidgetContents)
        self.scrollSpeed.setObjectName(u"scrollSpeed")
        self.scrollSpeed.setMinimum(1)
        self.scrollSpeed.setMaximum(4000)
        self.scrollSpeed.setValue(200)

        self.horizontalLayout_12.addWidget(self.scrollSpeed)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_13.addWidget(self.label_11)

        self.turnSpeed = WheelDoubleSpinBox(self.scrollAreaWidgetContents)
        self.turnSpeed.setObjectName(u"turnSpeed")
        self.turnSpeed.setMinimum(0.100000000000000)
        self.turnSpeed.setSingleStep(0.100000000000000)
        self.turnSpeed.setValue(5.000000000000000)

        self.horizontalLayout_13.addWidget(self.turnSpeed)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.line_8 = QFrame(self.scrollAreaWidgetContents)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_8)

        self.pushButton_2 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.fullButton = QPushButton(self.scrollAreaWidgetContents)
        self.fullButton.setObjectName(u"fullButton")

        self.verticalLayout.addWidget(self.fullButton)

        self.returePage = QPushButton(self.scrollAreaWidgetContents)
        self.returePage.setObjectName(u"returePage")
        self.returePage.setMinimumSize(QSize(0, 0))
        self.returePage.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.returePage)

        self.line_5 = QFrame(self.scrollAreaWidgetContents)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")

        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_4 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_5.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_5.addWidget(self.pushButton_5)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.line_7 = QFrame(self.scrollAreaWidgetContents)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lastPage = QPushButton(self.scrollAreaWidgetContents)
        self.lastPage.setObjectName(u"lastPage")
        self.lastPage.setMinimumSize(QSize(0, 0))
        self.lastPage.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.lastPage)

        self.nextPage = QPushButton(self.scrollAreaWidgetContents)
        self.nextPage.setObjectName(u"nextPage")
        self.nextPage.setMinimumSize(QSize(0, 0))
        self.nextPage.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.nextPage)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.scrollArea22.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea22, 0, 0, 1, 1)


        self.retranslateUi(ReadImg)
        self.pushButton_5.clicked.connect(ReadImg.OpenNextEps)
        self.lastPage.clicked.connect(ReadImg.LastPage)
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
        ReadImg.setWindowTitle(QCoreApplication.translate("ReadImg", u"\u5de5\u5177", None))
        self.label_4.setText(QCoreApplication.translate("ReadImg", u"\u56fe\u7247\u4fe1\u606f", None))
        self.epsLabel.setText(QCoreApplication.translate("ReadImg", u"\u4f4d\u7f6e\uff1a", None))
        self.stateLable.setText(QCoreApplication.translate("ReadImg", u"\u72b6\u6001\uff1a", None))
        self.sizeLabel.setText(QCoreApplication.translate("ReadImg", u"\u5927\u5c0f\uff1a", None))
        self.resolutionLabel.setText(QCoreApplication.translate("ReadImg", u"\u5206\u8fa8\u7387\uff1a", None))
        self.sizeLabel2.setText("")
        self.stateLable2.setText("")
        self.epsLabel2.setText("")
        self.resolutionLabel2.setText("")
        self.label.setText(QCoreApplication.translate("ReadImg", u"Waifu2x\u53c2\u6570", None))
        self.modelLabel.setText(QCoreApplication.translate("ReadImg", u"CUNET", None))
        self.modelBox.setItemText(0, QCoreApplication.translate("ReadImg", u"\u81ea\u52a8", None))
        self.modelBox.setItemText(1, QCoreApplication.translate("ReadImg", u"cunet", None))
        self.modelBox.setItemText(2, QCoreApplication.translate("ReadImg", u"photo", None))
        self.modelBox.setItemText(3, QCoreApplication.translate("ReadImg", u"anime_style_art_rgb", None))

        self.label_8.setText(QCoreApplication.translate("ReadImg", u"\u6a21\u578b\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("ReadImg", u"\u653e\u5927\u500d\u6570\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("ReadImg", u"\u8f6c\u6362\u6a21\u5f0f\uff1a", None))
        self.tickLabel.setText(QCoreApplication.translate("ReadImg", u"\u8017\u65f6\uff1a", None))
        self.waifu2xTick.setText("")
        self.gpuLabel.setText(QCoreApplication.translate("ReadImg", u"GPU", None))
        self.waifu2xRes.setText("")
        self.waifu2xStatus.setText("")
        self.waifu2xSave.setText(QCoreApplication.translate("ReadImg", u"\u4fee\u6539\u53c2\u6570", None))
        self.waifu2xCancle.setText(QCoreApplication.translate("ReadImg", u"\u4fdd\u5b58", None))
        self.waifu2xSize.setText("")
        self.label_2.setText(QCoreApplication.translate("ReadImg", u"\u53bb\u566a\u7b49\u7ea7\uff1a", None))
        self.checkBox.setText(QCoreApplication.translate("ReadImg", u"\u81ea\u52a8Waifu2x", None))
        self.curWaifu2x.setText(QCoreApplication.translate("ReadImg", u"\u672c\u5f20\u56fe\u5f00\u542fWaifu2x (F2)", None))
        self.stateWaifu.setText(QCoreApplication.translate("ReadImg", u"\u72b6\u6001\uff1a", None))
        self.resolutionWaifu.setText(QCoreApplication.translate("ReadImg", u"\u5206\u8fa8\u7387\uff1a", None))
        self.scaleLabel.setText(QCoreApplication.translate("ReadImg", u"2", None))
        self.sizeWaifu.setText(QCoreApplication.translate("ReadImg", u"\u5927\u5c0f\uff1a", None))
        self.noiseLabel.setText(QCoreApplication.translate("ReadImg", u"3", None))
        self.noiseBox.setItemText(0, QCoreApplication.translate("ReadImg", u"\u81ea\u52a8", None))
        self.noiseBox.setItemText(1, QCoreApplication.translate("ReadImg", u"0", None))
        self.noiseBox.setItemText(2, QCoreApplication.translate("ReadImg", u"1", None))
        self.noiseBox.setItemText(3, QCoreApplication.translate("ReadImg", u"2", None))
        self.noiseBox.setItemText(4, QCoreApplication.translate("ReadImg", u"3", None))

        self.preDownWaifu2x.setText(QCoreApplication.translate("ReadImg", u"\u4f18\u5148\u4f7f\u7528\u4e0b\u8f7d\u8f6c\u6362\u597d\u7684", None))
        self.label_6.setText(QCoreApplication.translate("ReadImg", u"\u7ffb\u9875\u8bbe\u7f6e", None))
        self.label_5.setText(QCoreApplication.translate("ReadImg", u"\u7ffb\u9875\u6a21\u5f0f\uff1a", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("ReadImg", u"\u4e0a\u4e0b\u6eda\u52a8", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("ReadImg", u"\u9ed8\u8ba4", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("ReadImg", u"\u5de6\u53f3\u53cc\u9875", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("ReadImg", u"\u53f3\u5de6\u53cc\u9875", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("ReadImg", u"\u5de6\u53f3\u6eda\u52a8", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("ReadImg", u"\u53f3\u5de6\u6eda\u52a8", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("ReadImg", u"\u53f3\u5de6\u53cc\u9875(\u6eda\u8f6e\u6b63\u5e8f)", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("ReadImg", u"\u7b49\u5bbd\u6a21\u5f0f", None))

        self.zoomLabel.setText(QCoreApplication.translate("ReadImg", u"\u7f29\u653e\uff08120%\uff09", None))
        self.label_7.setText(QCoreApplication.translate("ReadImg", u"\u81ea\u52a8\u6eda\u52a8/\u7ffb\u9875", None))
        self.label_10.setText(QCoreApplication.translate("ReadImg", u"\u6eda\u52a8\u901f\u5ea6\uff08\u50cf\u7d20\uff09\uff1a", None))
        self.label_11.setText(QCoreApplication.translate("ReadImg", u"\u7ffb\u9875\u901f\u5ea6\uff08\u79d2\uff09\uff1a", None))
        self.pushButton_2.setText(QCoreApplication.translate("ReadImg", u"\u9690\u85cf", None))
        self.fullButton.setText(QCoreApplication.translate("ReadImg", u"\u5168\u5c4f", None))
        self.returePage.setText(QCoreApplication.translate("ReadImg", u"\u8fd4\u56de", None))
        self.pushButton_4.setText(QCoreApplication.translate("ReadImg", u"\u4e0a\u4e00\u7ae0", None))
        self.pushButton_5.setText(QCoreApplication.translate("ReadImg", u"\u4e0b\u4e00\u7ae0", None))
        self.lastPage.setText(QCoreApplication.translate("ReadImg", u"\u4e0a\u4e00\u9875", None))
        self.nextPage.setText(QCoreApplication.translate("ReadImg", u"\u4e0b\u4e00\u9875", None))
    # retranslateUi

