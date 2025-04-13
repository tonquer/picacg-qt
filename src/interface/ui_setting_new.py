# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_setting_new.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QCommandLinkButton,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

from component.box.wheel_combo_box import WheelComboBox
from component.box.wheel_double_spin_box import WheelDoubleSpinBox
from component.box.wheel_spin_box import WheelSpinBox
from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_SettingNew(object):
    def setupUi(self, SettingNew):
        if not SettingNew.objectName():
            SettingNew.setObjectName(u"SettingNew")
        SettingNew.resize(946, 789)
        SettingNew.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(SettingNew)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.msgLabel = QLabel(SettingNew)
        self.msgLabel.setObjectName(u"msgLabel")
        self.msgLabel.setEnabled(True)
        self.msgLabel.setStyleSheet(u"color: rgb(255, 0, 0);")

        self.verticalLayout_2.addWidget(self.msgLabel, 0, Qt.AlignLeft)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.generalButton = QCommandLinkButton(SettingNew)
        self.generalButton.setObjectName(u"generalButton")

        self.verticalLayout.addWidget(self.generalButton)

        self.proxyButton = QCommandLinkButton(SettingNew)
        self.proxyButton.setObjectName(u"proxyButton")

        self.verticalLayout.addWidget(self.proxyButton)

        self.waifu2xButton = QCommandLinkButton(SettingNew)
        self.waifu2xButton.setObjectName(u"waifu2xButton")

        self.verticalLayout.addWidget(self.waifu2xButton)

        self.downloadButton = QCommandLinkButton(SettingNew)
        self.downloadButton.setObjectName(u"downloadButton")

        self.verticalLayout.addWidget(self.downloadButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.scrollArea = SmoothScrollArea(SettingNew)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u".QFrame\n"
"        {\n"
"            background-color: rgb(253, 253, 253);\n"
"            \n"
"            border:2px solid rgb(234,234,234);\n"
"            border-radius:5px\n"
"        }        ")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -406, 727, 2834))
        self.scrollAreaWidgetContents.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.generalLabel = QLabel(self.scrollAreaWidgetContents)
        self.generalLabel.setObjectName(u"generalLabel")
        font = QFont()
        font.setPointSize(18)
        self.generalLabel.setFont(font)

        self.verticalLayout_4.addWidget(self.generalLabel)

        self.frame_1 = QFrame(self.scrollAreaWidgetContents)
        self.frame_1.setObjectName(u"frame_1")
        font1 = QFont()
        font1.setPointSize(12)
        self.frame_1.setFont(font1)
        self.frame_1.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.frame_1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_update = QLabel(self.frame_1)
        self.label_update.setObjectName(u"label_update")
        self.label_update.setMaximumSize(QSize(16777215, 19))
        self.label_update.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_update)

        self.checkBox_IsUpdate = QCheckBox(self.frame_1)
        self.checkBox_IsUpdate.setObjectName(u"checkBox_IsUpdate")

        self.verticalLayout_3.addWidget(self.checkBox_IsUpdate)


        self.verticalLayout_4.addWidget(self.frame_1)

        self.frame_16 = QFrame(self.scrollAreaWidgetContents)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frame_16)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.label_37 = QLabel(self.frame_16)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setMaximumSize(QSize(16777215, 19))
        self.label_37.setFont(font1)

        self.verticalLayout_20.addWidget(self.label_37)

        self.grabGestureBox = QCheckBox(self.frame_16)
        self.grabGestureBox.setObjectName(u"grabGestureBox")

        self.verticalLayout_20.addWidget(self.grabGestureBox)


        self.verticalLayout_4.addWidget(self.frame_16)

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFont(font1)
        self.frame_2.setStyleSheet(u"")
        self.verticalLayout_5 = QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(16777215, 21))
        self.label_6.setFont(font1)

        self.verticalLayout_5.addWidget(self.label_6)

        self.themeButton0 = QRadioButton(self.frame_2)
        self.themeGroup = QButtonGroup(SettingNew)
        self.themeGroup.setObjectName(u"themeGroup")
        self.themeGroup.addButton(self.themeButton0)
        self.themeButton0.setObjectName(u"themeButton0")
        self.themeButton0.setChecked(True)

        self.verticalLayout_5.addWidget(self.themeButton0)

        self.themeButton2 = QRadioButton(self.frame_2)
        self.themeGroup.addButton(self.themeButton2)
        self.themeButton2.setObjectName(u"themeButton2")

        self.verticalLayout_5.addWidget(self.themeButton2)

        self.themeButton1 = QRadioButton(self.frame_2)
        self.themeGroup.addButton(self.themeButton1)
        self.themeButton1.setObjectName(u"themeButton1")

        self.verticalLayout_5.addWidget(self.themeButton1)


        self.verticalLayout_4.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.scrollAreaWidgetContents)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFont(font1)
        self.frame_3.setStyleSheet(u"")
        self.verticalLayout_6 = QVBoxLayout(self.frame_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_lang = QLabel(self.frame_3)
        self.label_lang.setObjectName(u"label_lang")
        self.label_lang.setFont(font1)

        self.verticalLayout_6.addWidget(self.label_lang)

        self.languageButton0 = QRadioButton(self.frame_3)
        self.languageGroup = QButtonGroup(SettingNew)
        self.languageGroup.setObjectName(u"languageGroup")
        self.languageGroup.addButton(self.languageButton0)
        self.languageButton0.setObjectName(u"languageButton0")
        self.languageButton0.setChecked(True)

        self.verticalLayout_6.addWidget(self.languageButton0)

        self.languageButton1 = QRadioButton(self.frame_3)
        self.languageGroup.addButton(self.languageButton1)
        self.languageButton1.setObjectName(u"languageButton1")

        self.verticalLayout_6.addWidget(self.languageButton1)

        self.languageButton2 = QRadioButton(self.frame_3)
        self.languageGroup.addButton(self.languageButton2)
        self.languageButton2.setObjectName(u"languageButton2")

        self.verticalLayout_6.addWidget(self.languageButton2)

        self.languageButton3 = QRadioButton(self.frame_3)
        self.languageGroup.addButton(self.languageButton3)
        self.languageButton3.setObjectName(u"languageButton3")

        self.verticalLayout_6.addWidget(self.languageButton3)


        self.verticalLayout_4.addWidget(self.frame_3)

        self.frame_7 = QFrame(self.scrollAreaWidgetContents)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_7)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.label_8 = QLabel(self.frame_7)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)

        self.verticalLayout_18.addWidget(self.label_8)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_33 = QLabel(self.frame_7)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_3.addWidget(self.label_33)

        self.fontBox = WheelComboBox(self.frame_7)
        self.fontBox.addItem("")
        self.fontBox.setObjectName(u"fontBox")
        self.fontBox.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_3.addWidget(self.fontBox)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_23)


        self.verticalLayout_18.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.label_34 = QLabel(self.frame_7)
        self.label_34.setObjectName(u"label_34")

        self.horizontalLayout_25.addWidget(self.label_34)

        self.fontSize = WheelComboBox(self.frame_7)
        self.fontSize.addItem("")
        self.fontSize.addItem("")
        self.fontSize.addItem("")
        self.fontSize.addItem("")
        self.fontSize.addItem("")
        self.fontSize.addItem("")
        self.fontSize.addItem("")
        self.fontSize.addItem("")
        self.fontSize.addItem("")
        self.fontSize.addItem("")
        self.fontSize.addItem("")
        self.fontSize.addItem("")
        self.fontSize.setObjectName(u"fontSize")
        self.fontSize.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_25.addWidget(self.fontSize)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_24)


        self.verticalLayout_18.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_35 = QLabel(self.frame_7)
        self.label_35.setObjectName(u"label_35")

        self.horizontalLayout_26.addWidget(self.label_35)

        self.fontStyle = WheelComboBox(self.frame_7)
        self.fontStyle.addItem("")
        self.fontStyle.addItem("")
        self.fontStyle.addItem("")
        self.fontStyle.addItem("")
        self.fontStyle.addItem("")
        self.fontStyle.addItem("")
        self.fontStyle.setObjectName(u"fontStyle")
        self.fontStyle.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_26.addWidget(self.fontStyle)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_25)


        self.verticalLayout_18.addLayout(self.horizontalLayout_26)


        self.verticalLayout_4.addWidget(self.frame_7)

        self.frame_18 = QFrame(self.scrollAreaWidgetContents)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFont(font1)
        self.frame_18.setStyleSheet(u"")
        self.verticalLayout_22 = QVBoxLayout(self.frame_18)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.label_13 = QLabel(self.frame_18)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font1)

        self.verticalLayout_22.addWidget(self.label_13)

        self.mainScaleBox = QCheckBox(self.frame_18)
        self.mainScaleBox.setObjectName(u"mainScaleBox")

        self.verticalLayout_22.addWidget(self.mainScaleBox)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_17 = QLabel(self.frame_18)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_4.addWidget(self.label_17)

        self.scaleBox = WheelSpinBox(self.frame_18)
        self.scaleBox.setObjectName(u"scaleBox")
        self.scaleBox.setMinimum(50)
        self.scaleBox.setMaximum(300)
        self.scaleBox.setValue(100)

        self.horizontalLayout_4.addWidget(self.scaleBox)


        self.verticalLayout_22.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addWidget(self.frame_18)

        self.frame_17 = QFrame(self.scrollAreaWidgetContents)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.frame_17)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.label_38 = QLabel(self.frame_17)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setFont(font1)

        self.verticalLayout_21.addWidget(self.label_38)

        self.showCloseButton0 = QRadioButton(self.frame_17)
        self.showCloseButtonGroup = QButtonGroup(SettingNew)
        self.showCloseButtonGroup.setObjectName(u"showCloseButtonGroup")
        self.showCloseButtonGroup.addButton(self.showCloseButton0)
        self.showCloseButton0.setObjectName(u"showCloseButton0")

        self.verticalLayout_21.addWidget(self.showCloseButton0)

        self.showCloseButton1 = QRadioButton(self.frame_17)
        self.showCloseButtonGroup.addButton(self.showCloseButton1)
        self.showCloseButton1.setObjectName(u"showCloseButton1")

        self.verticalLayout_21.addWidget(self.showCloseButton1)


        self.verticalLayout_4.addWidget(self.frame_17)

        self.frame_14 = QFrame(self.scrollAreaWidgetContents)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFont(font1)
        self.frame_14.setStyleSheet(u"")
        self.verticalLayout_17 = QVBoxLayout(self.frame_14)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.label_2 = QLabel(self.frame_14)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.verticalLayout_17.addWidget(self.label_2)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.coverSize = WheelSpinBox(self.frame_14)
        self.coverSize.setObjectName(u"coverSize")
        self.coverSize.setMinimumSize(QSize(140, 0))
        self.coverSize.setMinimum(50)
        self.coverSize.setMaximum(250)
        self.coverSize.setSingleStep(10)
        self.coverSize.setValue(100)

        self.horizontalLayout_15.addWidget(self.coverSize)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_13)


        self.verticalLayout_17.addLayout(self.horizontalLayout_15)

        self.label_29 = QLabel(self.frame_14)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font1)

        self.verticalLayout_17.addWidget(self.label_29)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.categorySize = WheelSpinBox(self.frame_14)
        self.categorySize.setObjectName(u"categorySize")
        self.categorySize.setMinimumSize(QSize(140, 0))
        self.categorySize.setMinimum(30)
        self.categorySize.setMaximum(250)
        self.categorySize.setSingleStep(10)
        self.categorySize.setValue(80)

        self.horizontalLayout_22.addWidget(self.categorySize)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_21)


        self.verticalLayout_17.addLayout(self.horizontalLayout_22)

        self.label_44 = QLabel(self.frame_14)
        self.label_44.setObjectName(u"label_44")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.label_44.setFont(font2)

        self.verticalLayout_17.addWidget(self.label_44)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.titleLineBox = WheelComboBox(self.frame_14)
        self.titleLineBox.addItem("")
        self.titleLineBox.addItem("")
        self.titleLineBox.addItem("")
        self.titleLineBox.addItem("")
        self.titleLineBox.addItem("")
        self.titleLineBox.setObjectName(u"titleLineBox")

        self.horizontalLayout_34.addWidget(self.titleLineBox)

        self.horizontalSpacer_32 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_32)


        self.verticalLayout_17.addLayout(self.horizontalLayout_34)

        self.label_45 = QLabel(self.frame_14)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFont(font2)

        self.verticalLayout_17.addWidget(self.label_45)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.categoryBox = WheelComboBox(self.frame_14)
        self.categoryBox.addItem("")
        self.categoryBox.addItem("")
        self.categoryBox.setObjectName(u"categoryBox")

        self.horizontalLayout_35.addWidget(self.categoryBox)

        self.horizontalSpacer_33 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_33)


        self.verticalLayout_17.addLayout(self.horizontalLayout_35)

        self.label_40 = QLabel(self.frame_14)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setFont(font2)

        self.verticalLayout_17.addWidget(self.label_40)

        self.openglBox = QCheckBox(self.frame_14)
        self.openglBox.setObjectName(u"openglBox")

        self.verticalLayout_17.addWidget(self.openglBox)


        self.verticalLayout_4.addWidget(self.frame_14)

        self.frame_4 = QFrame(self.scrollAreaWidgetContents)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFont(font1)
        self.frame_4.setStyleSheet(u"")
        self.verticalLayout_7 = QVBoxLayout(self.frame_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(16777215, 21))
        self.label_10.setFont(font1)

        self.verticalLayout_7.addWidget(self.label_10)

        self.logutton0 = QRadioButton(self.frame_4)
        self.logGroup = QButtonGroup(SettingNew)
        self.logGroup.setObjectName(u"logGroup")
        self.logGroup.addButton(self.logutton0)
        self.logutton0.setObjectName(u"logutton0")
        self.logutton0.setChecked(True)

        self.verticalLayout_7.addWidget(self.logutton0)

        self.logutton1 = QRadioButton(self.frame_4)
        self.logGroup.addButton(self.logutton1)
        self.logutton1.setObjectName(u"logutton1")

        self.verticalLayout_7.addWidget(self.logutton1)

        self.logutton2 = QRadioButton(self.frame_4)
        self.logGroup.addButton(self.logutton2)
        self.logutton2.setObjectName(u"logutton2")

        self.verticalLayout_7.addWidget(self.logutton2)


        self.verticalLayout_4.addWidget(self.frame_4)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.proxyLabel = QLabel(self.scrollAreaWidgetContents)
        self.proxyLabel.setObjectName(u"proxyLabel")
        self.proxyLabel.setFont(font)

        self.verticalLayout_4.addWidget(self.proxyLabel)

        self.frame_5 = QFrame(self.scrollAreaWidgetContents)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFont(font1)
        self.frame_5.setStyleSheet(u"")
        self.verticalLayout_8 = QVBoxLayout(self.frame_5)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 26))
        self.label_7.setFont(font1)

        self.verticalLayout_8.addWidget(self.label_7)

        self.proxy0 = QRadioButton(self.frame_5)
        self.proxyGroup = QButtonGroup(SettingNew)
        self.proxyGroup.setObjectName(u"proxyGroup")
        self.proxyGroup.addButton(self.proxy0)
        self.proxy0.setObjectName(u"proxy0")

        self.verticalLayout_8.addWidget(self.proxy0)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.proxy1 = QRadioButton(self.frame_5)
        self.proxyGroup.addButton(self.proxy1)
        self.proxy1.setObjectName(u"proxy1")
        self.proxy1.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_23.addWidget(self.proxy1)

        self.line_5 = QFrame(self.frame_5)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_23.addWidget(self.line_5)

        self.label_31 = QLabel(self.frame_5)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_23.addWidget(self.label_31)

        self.httpEdit = QLineEdit(self.frame_5)
        self.httpEdit.setObjectName(u"httpEdit")

        self.horizontalLayout_23.addWidget(self.httpEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer)


        self.verticalLayout_8.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.proxy2 = QRadioButton(self.frame_5)
        self.proxyGroup.addButton(self.proxy2)
        self.proxy2.setObjectName(u"proxy2")
        self.proxy2.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_24.addWidget(self.proxy2)

        self.line_6 = QFrame(self.frame_5)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_24.addWidget(self.line_6)

        self.label_32 = QLabel(self.frame_5)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_24.addWidget(self.label_32)

        self.sockEdit = QLineEdit(self.frame_5)
        self.sockEdit.setObjectName(u"sockEdit")

        self.horizontalLayout_24.addWidget(self.sockEdit)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_22)


        self.verticalLayout_8.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.proxy3 = QRadioButton(self.frame_5)
        self.proxyGroup.addButton(self.proxy3)
        self.proxy3.setObjectName(u"proxy3")

        self.horizontalLayout_27.addWidget(self.proxy3)


        self.verticalLayout_8.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.openProxy = QPushButton(self.frame_5)
        self.openProxy.setObjectName(u"openProxy")

        self.horizontalLayout_28.addWidget(self.openProxy)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_26)


        self.verticalLayout_8.addLayout(self.horizontalLayout_28)


        self.verticalLayout_4.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.scrollAreaWidgetContents)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFont(font1)
        self.frame_6.setStyleSheet(u"")
        self.verticalLayout_9 = QVBoxLayout(self.frame_6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_9 = QLabel(self.frame_6)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(16777215, 19))
        self.label_9.setFont(font1)

        self.verticalLayout_9.addWidget(self.label_9)

        self.chatProxy = QCheckBox(self.frame_6)
        self.chatProxy.setObjectName(u"chatProxy")
        self.chatProxy.setChecked(False)

        self.verticalLayout_9.addWidget(self.chatProxy)


        self.verticalLayout_4.addWidget(self.frame_6)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.line_3 = QFrame(self.scrollAreaWidgetContents)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.waifu2xLabel = QLabel(self.scrollAreaWidgetContents)
        self.waifu2xLabel.setObjectName(u"waifu2xLabel")
        self.waifu2xLabel.setFont(font)

        self.verticalLayout_4.addWidget(self.waifu2xLabel)

        self.frame_10 = QFrame(self.scrollAreaWidgetContents)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFont(font1)
        self.frame_10.setStyleSheet(u"")
        self.verticalLayout_12 = QVBoxLayout(self.frame_10)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_20 = QLabel(self.frame_10)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMaximumSize(QSize(16777215, 21))
        self.label_20.setFont(font1)

        self.verticalLayout_12.addWidget(self.label_20)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.encodeSelect = WheelComboBox(self.frame_10)
        self.encodeSelect.setObjectName(u"encodeSelect")
        self.encodeSelect.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_17.addWidget(self.encodeSelect)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_14)


        self.verticalLayout_12.addLayout(self.horizontalLayout_17)

        self.label_11 = QLabel(self.frame_10)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(16777215, 21))
        self.label_11.setFont(font1)

        self.verticalLayout_12.addWidget(self.label_11)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.threadSelect = WheelComboBox(self.frame_10)
        self.threadSelect.addItem("")
        self.threadSelect.setObjectName(u"threadSelect")
        self.threadSelect.setMinimumSize(QSize(150, 0))
        self.threadSelect.setFocusPolicy(Qt.StrongFocus)

        self.horizontalLayout_16.addWidget(self.threadSelect)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_15)


        self.verticalLayout_12.addLayout(self.horizontalLayout_16)

        self.label_39 = QLabel(self.frame_10)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFont(font1)

        self.verticalLayout_12.addWidget(self.label_39)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.tileComboBox = WheelComboBox(self.frame_10)
        self.tileComboBox.addItem("")
        self.tileComboBox.addItem("")
        self.tileComboBox.addItem("")
        self.tileComboBox.addItem("")
        self.tileComboBox.setObjectName(u"tileComboBox")

        self.horizontalLayout_29.addWidget(self.tileComboBox)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_27)


        self.verticalLayout_12.addLayout(self.horizontalLayout_29)


        self.verticalLayout_4.addWidget(self.frame_10)

        self.frame_8 = QFrame(self.scrollAreaWidgetContents)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFont(font1)
        self.frame_8.setStyleSheet(u"")
        self.verticalLayout_10 = QVBoxLayout(self.frame_8)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_12 = QLabel(self.frame_8)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMaximumSize(QSize(16777215, 84))
        self.label_12.setFont(font1)

        self.verticalLayout_10.addWidget(self.label_12)

        self.readCheckBox = QCheckBox(self.frame_8)
        self.readCheckBox.setObjectName(u"readCheckBox")

        self.verticalLayout_10.addWidget(self.readCheckBox)

        self.preDownWaifu2x = QCheckBox(self.frame_8)
        self.preDownWaifu2x.setObjectName(u"preDownWaifu2x")

        self.verticalLayout_10.addWidget(self.preDownWaifu2x)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_28 = QLabel(self.frame_8)
        self.label_28.setObjectName(u"label_28")

        self.horizontalLayout_21.addWidget(self.label_28)

        self.lookMaxBox = WheelSpinBox(self.frame_8)
        self.lookMaxBox.setObjectName(u"lookMaxBox")
        self.lookMaxBox.setMinimumSize(QSize(80, 0))
        self.lookMaxBox.setMinimum(360)
        self.lookMaxBox.setMaximum(10000)
        self.lookMaxBox.setValue(4096)

        self.horizontalLayout_21.addWidget(self.lookMaxBox)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_20)


        self.verticalLayout_10.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_14 = QLabel(self.frame_8)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(60, 0))
        self.label_14.setMaximumSize(QSize(156, 16777215))

        self.horizontalLayout_5.addWidget(self.label_14)

        self.readModelName = QToolButton(self.frame_8)
        self.readModelName.setObjectName(u"readModelName")

        self.horizontalLayout_5.addWidget(self.readModelName)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_10.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_15 = QLabel(self.frame_8)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(60, 0))
        self.label_15.setMaximumSize(QSize(156, 16777215))

        self.horizontalLayout_6.addWidget(self.label_15)

        self.readScale = WheelDoubleSpinBox(self.frame_8)
        self.readScale.setObjectName(u"readScale")
        self.readScale.setMinimumSize(QSize(150, 0))
        self.readScale.setDecimals(1)
        self.readScale.setMaximum(32.000000000000000)
        self.readScale.setSingleStep(0.100000000000000)
        self.readScale.setValue(2.000000000000000)

        self.horizontalLayout_6.addWidget(self.readScale)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)


        self.verticalLayout_10.addLayout(self.horizontalLayout_6)


        self.verticalLayout_4.addWidget(self.frame_8)

        self.frame_12 = QFrame(self.scrollAreaWidgetContents)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFont(font1)
        self.frame_12.setStyleSheet(u"")
        self.verticalLayout_15 = QVBoxLayout(self.frame_12)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label_24 = QLabel(self.frame_12)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMaximumSize(QSize(16777215, 84))
        self.label_24.setFont(font1)

        self.verticalLayout_15.addWidget(self.label_24)

        self.coverCheckBox = QCheckBox(self.frame_12)
        self.coverCheckBox.setObjectName(u"coverCheckBox")

        self.verticalLayout_15.addWidget(self.coverCheckBox)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_22 = QLabel(self.frame_12)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_11.addWidget(self.label_22)

        self.coverMaxBox = WheelSpinBox(self.frame_12)
        self.coverMaxBox.setObjectName(u"coverMaxBox")
        self.coverMaxBox.setMinimumSize(QSize(80, 0))
        self.coverMaxBox.setMinimum(100)
        self.coverMaxBox.setMaximum(2560)
        self.coverMaxBox.setValue(400)

        self.horizontalLayout_11.addWidget(self.coverMaxBox)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_9)


        self.verticalLayout_15.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_25 = QLabel(self.frame_12)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(60, 0))
        self.label_25.setMaximumSize(QSize(156, 16777215))

        self.horizontalLayout_13.addWidget(self.label_25)

        self.coverModelName = QToolButton(self.frame_12)
        self.coverModelName.setObjectName(u"coverModelName")

        self.horizontalLayout_13.addWidget(self.coverModelName)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_11)


        self.verticalLayout_15.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_26 = QLabel(self.frame_12)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(60, 0))
        self.label_26.setMaximumSize(QSize(156, 16777215))

        self.horizontalLayout_14.addWidget(self.label_26)

        self.coverScale = WheelDoubleSpinBox(self.frame_12)
        self.coverScale.setObjectName(u"coverScale")
        self.coverScale.setMinimumSize(QSize(150, 0))
        self.coverScale.setDecimals(1)
        self.coverScale.setMaximum(32.000000000000000)
        self.coverScale.setSingleStep(0.100000000000000)
        self.coverScale.setValue(2.000000000000000)

        self.horizontalLayout_14.addWidget(self.coverScale)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_12)


        self.verticalLayout_15.addLayout(self.horizontalLayout_14)


        self.verticalLayout_4.addWidget(self.frame_12)

        self.frame_9 = QFrame(self.scrollAreaWidgetContents)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFont(font1)
        self.frame_9.setStyleSheet(u"")
        self.verticalLayout_11 = QVBoxLayout(self.frame_9)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_16 = QLabel(self.frame_9)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMaximumSize(QSize(16777215, 110))
        self.label_16.setFont(font1)

        self.verticalLayout_11.addWidget(self.label_16)

        self.downAuto = QCheckBox(self.frame_9)
        self.downAuto.setObjectName(u"downAuto")
        self.downAuto.setChecked(True)

        self.verticalLayout_11.addWidget(self.downAuto)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_18 = QLabel(self.frame_9)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(60, 0))
        self.label_18.setMaximumSize(QSize(156, 16777215))

        self.horizontalLayout_9.addWidget(self.label_18)

        self.downModelName = QToolButton(self.frame_9)
        self.downModelName.setObjectName(u"downModelName")

        self.horizontalLayout_9.addWidget(self.downModelName)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)


        self.verticalLayout_11.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_19 = QLabel(self.frame_9)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(60, 0))
        self.label_19.setMaximumSize(QSize(156, 16777215))

        self.horizontalLayout_7.addWidget(self.label_19)

        self.downScale = WheelDoubleSpinBox(self.frame_9)
        self.downScale.setObjectName(u"downScale")
        self.downScale.setMinimumSize(QSize(150, 0))
        self.downScale.setDecimals(1)
        self.downScale.setMaximum(32.000000000000000)
        self.downScale.setSingleStep(0.100000000000000)
        self.downScale.setValue(2.000000000000000)

        self.horizontalLayout_7.addWidget(self.downScale)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)


        self.verticalLayout_11.addLayout(self.horizontalLayout_7)


        self.verticalLayout_4.addWidget(self.frame_9)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_4)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)

        self.downloadLabel = QLabel(self.scrollAreaWidgetContents)
        self.downloadLabel.setObjectName(u"downloadLabel")
        self.downloadLabel.setFont(font)

        self.verticalLayout_4.addWidget(self.downloadLabel)

        self.frame_15 = QFrame(self.scrollAreaWidgetContents)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.frame_15)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.label_36 = QLabel(self.frame_15)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMaximumSize(QSize(16777215, 32))
        self.label_36.setFont(font1)

        self.verticalLayout_19.addWidget(self.label_36)

        self.saveNameButton0 = QRadioButton(self.frame_15)
        self.saveNameGroup = QButtonGroup(SettingNew)
        self.saveNameGroup.setObjectName(u"saveNameGroup")
        self.saveNameGroup.addButton(self.saveNameButton0)
        self.saveNameButton0.setObjectName(u"saveNameButton0")
        self.saveNameButton0.setChecked(True)

        self.verticalLayout_19.addWidget(self.saveNameButton0)

        self.saveNameButton1 = QRadioButton(self.frame_15)
        self.saveNameGroup.addButton(self.saveNameButton1)
        self.saveNameButton1.setObjectName(u"saveNameButton1")

        self.verticalLayout_19.addWidget(self.saveNameButton1)

        self.saveNameButton2 = QRadioButton(self.frame_15)
        self.saveNameGroup.addButton(self.saveNameButton2)
        self.saveNameButton2.setObjectName(u"saveNameButton2")

        self.verticalLayout_19.addWidget(self.saveNameButton2)


        self.verticalLayout_4.addWidget(self.frame_15)

        self.frame_11 = QFrame(self.scrollAreaWidgetContents)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFont(font1)
        self.frame_11.setStyleSheet(u"")
        self.verticalLayout_13 = QVBoxLayout(self.frame_11)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_21 = QLabel(self.frame_11)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMaximumSize(QSize(16777215, 32))
        self.label_21.setFont(font1)

        self.verticalLayout_13.addWidget(self.label_21)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.setDirButton = QPushButton(self.frame_11)
        self.setDirButton.setObjectName(u"setDirButton")

        self.horizontalLayout_10.addWidget(self.setDirButton)

        self.setLogDirButton = QPushButton(self.frame_11)
        self.setLogDirButton.setObjectName(u"setLogDirButton")

        self.horizontalLayout_10.addWidget(self.setLogDirButton)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_8)


        self.verticalLayout_13.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.frame_11)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_2.addWidget(self.label_3)

        self.downloadDir = QLabel(self.frame_11)
        self.downloadDir.setObjectName(u"downloadDir")
        self.downloadDir.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_2.addWidget(self.downloadDir)

        self.openDownloadDir = QPushButton(self.frame_11)
        self.openDownloadDir.setObjectName(u"openDownloadDir")

        self.horizontalLayout_2.addWidget(self.openDownloadDir)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_16)


        self.verticalLayout_13.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_4 = QLabel(self.frame_11)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_18.addWidget(self.label_4)

        self.cacheDir = QLabel(self.frame_11)
        self.cacheDir.setObjectName(u"cacheDir")
        self.cacheDir.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_18.addWidget(self.cacheDir)

        self.openCacheDir = QPushButton(self.frame_11)
        self.openCacheDir.setObjectName(u"openCacheDir")

        self.horizontalLayout_18.addWidget(self.openCacheDir)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_17)


        self.verticalLayout_13.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_27 = QLabel(self.frame_11)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_20.addWidget(self.label_27)

        self.chatDir = QLabel(self.frame_11)
        self.chatDir.setObjectName(u"chatDir")
        self.chatDir.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_20.addWidget(self.chatDir)

        self.openChatDir = QPushButton(self.frame_11)
        self.openChatDir.setObjectName(u"openChatDir")

        self.horizontalLayout_20.addWidget(self.openChatDir)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_18)


        self.verticalLayout_13.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_5 = QLabel(self.frame_11)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_19.addWidget(self.label_5)

        self.waifu2xDir = QLabel(self.frame_11)
        self.waifu2xDir.setObjectName(u"waifu2xDir")
        self.waifu2xDir.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_19.addWidget(self.waifu2xDir)

        self.openWaifu2xDir = QPushButton(self.frame_11)
        self.openWaifu2xDir.setObjectName(u"openWaifu2xDir")

        self.horizontalLayout_19.addWidget(self.openWaifu2xDir)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_19)


        self.verticalLayout_13.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_42 = QLabel(self.frame_11)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_31.addWidget(self.label_42)

        self.logLabel = QLabel(self.frame_11)
        self.logLabel.setObjectName(u"logLabel")
        self.logLabel.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_31.addWidget(self.logLabel)

        self.openLogDir = QPushButton(self.frame_11)
        self.openLogDir.setObjectName(u"openLogDir")

        self.horizontalLayout_31.addWidget(self.openLogDir)

        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_28)


        self.verticalLayout_13.addLayout(self.horizontalLayout_31)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")

        self.verticalLayout_13.addLayout(self.horizontalLayout_30)


        self.verticalLayout_4.addWidget(self.frame_11)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(SettingNew)

        QMetaObject.connectSlotsByName(SettingNew)
    # setupUi

    def retranslateUi(self, SettingNew):
        SettingNew.setWindowTitle(QCoreApplication.translate("SettingNew", u"\u8bbe\u7f6e", None))
        self.msgLabel.setText(QCoreApplication.translate("SettingNew", u"\u4f60\u4fee\u6539\u7684\u90e8\u5206\u8bbe\u7f6e\uff0c\u9700\u8981\u91cd\u542f\u751f\u6548", None))
        self.generalButton.setText(QCoreApplication.translate("SettingNew", u"\u901a\u7528", None))
        self.proxyButton.setText(QCoreApplication.translate("SettingNew", u"\u4ee3\u7406", None))
        self.waifu2xButton.setText(QCoreApplication.translate("SettingNew", u"Waifu2x", None))
        self.downloadButton.setText(QCoreApplication.translate("SettingNew", u"\u4e0b\u8f7d\u4e0e\u7f13\u5b58", None))
        self.generalLabel.setText(QCoreApplication.translate("SettingNew", u"\u901a\u7528", None))
        self.label_update.setText(QCoreApplication.translate("SettingNew", u"\u66f4\u65b0\uff1a", None))
        self.checkBox_IsUpdate.setText(QCoreApplication.translate("SettingNew", u"\u542f\u52a8\u65f6\u68c0\u67e5\u66f4\u65b0", None))
        self.label_37.setText(QCoreApplication.translate("SettingNew", u"\u89e6\u63a7\uff08\u91cd\u542f\u751f\u6548\uff09\uff1a", None))
        self.grabGestureBox.setText(QCoreApplication.translate("SettingNew", u"\u542f\u7528\u89e6\u63a7\u4f18\u5316", None))
        self.label_6.setText(QCoreApplication.translate("SettingNew", u"\u4e3b\u9898\uff1a", None))
        self.themeButton0.setText(QCoreApplication.translate("SettingNew", u"\u8ddf\u968f\u7cfb\u7edf", None))
        self.themeButton2.setText(QCoreApplication.translate("SettingNew", u"\u767d", None))
        self.themeButton1.setText(QCoreApplication.translate("SettingNew", u"\u9ed1", None))
        self.label_lang.setText(QCoreApplication.translate("SettingNew", u"\u8bed\u8a00\uff1a", None))
        self.languageButton0.setText(QCoreApplication.translate("SettingNew", u"\u6839\u636e\u7cfb\u7edf", None))
        self.languageButton1.setText(QCoreApplication.translate("SettingNew", u"\u7b80\u4f53\u4e2d\u6587", None))
        self.languageButton2.setText(QCoreApplication.translate("SettingNew", u"\u7e41\u9ad4\u4e2d\u6587", None))
        self.languageButton3.setText(QCoreApplication.translate("SettingNew", u"English", None))
        self.label_8.setText(QCoreApplication.translate("SettingNew", u"\u5b57\u4f53\uff08\u91cd\u542f\u751f\u6548\uff09\uff1a", None))
        self.label_33.setText(QCoreApplication.translate("SettingNew", u"\u5b57\u4f53\u9009\u62e9\uff1a", None))
        self.fontBox.setItemText(0, QCoreApplication.translate("SettingNew", u"\u9ed8\u8ba4", None))

        self.label_34.setText(QCoreApplication.translate("SettingNew", u"\u5b57\u4f53\u5927\u5c0f\uff1a", None))
        self.fontSize.setItemText(0, QCoreApplication.translate("SettingNew", u"\u9ed8\u8ba4", None))
        self.fontSize.setItemText(1, QCoreApplication.translate("SettingNew", u"9", None))
        self.fontSize.setItemText(2, QCoreApplication.translate("SettingNew", u"12", None))
        self.fontSize.setItemText(3, QCoreApplication.translate("SettingNew", u"14", None))
        self.fontSize.setItemText(4, QCoreApplication.translate("SettingNew", u"16", None))
        self.fontSize.setItemText(5, QCoreApplication.translate("SettingNew", u"18", None))
        self.fontSize.setItemText(6, QCoreApplication.translate("SettingNew", u"20", None))
        self.fontSize.setItemText(7, QCoreApplication.translate("SettingNew", u"22", None))
        self.fontSize.setItemText(8, QCoreApplication.translate("SettingNew", u"24", None))
        self.fontSize.setItemText(9, QCoreApplication.translate("SettingNew", u"26", None))
        self.fontSize.setItemText(10, QCoreApplication.translate("SettingNew", u"28", None))
        self.fontSize.setItemText(11, QCoreApplication.translate("SettingNew", u"30", None))

        self.label_35.setText(QCoreApplication.translate("SettingNew", u"\u5b57\u4f53\u7c97\u7ec6\uff1a", None))
        self.fontStyle.setItemText(0, QCoreApplication.translate("SettingNew", u"\u9ed8\u8ba4", None))
        self.fontStyle.setItemText(1, QCoreApplication.translate("SettingNew", u"\u9ad8\u4eae", None))
        self.fontStyle.setItemText(2, QCoreApplication.translate("SettingNew", u"\u6b63\u5e38", None))
        self.fontStyle.setItemText(3, QCoreApplication.translate("SettingNew", u"\u534a\u7c97\u4f53", None))
        self.fontStyle.setItemText(4, QCoreApplication.translate("SettingNew", u"\u7c97\u4f53", None))
        self.fontStyle.setItemText(5, QCoreApplication.translate("SettingNew", u"\u9ed1\u4f53", None))

        self.label_13.setText(QCoreApplication.translate("SettingNew", u"\u754c\u9762\u7f29\u653e\u663e\u793a\uff08\u9700\u91cd\u542f\u751f\u6548\uff09\uff1a", None))
        self.mainScaleBox.setText(QCoreApplication.translate("SettingNew", u"\u662f\u5426\u4f7f\u7528\u81ea\u5b9a\u4e49\u7f29\u653e\u6bd4\u4f8b", None))
        self.label_17.setText(QCoreApplication.translate("SettingNew", u"\u7f29\u653e\u6bd4\u4f8b\uff1a", None))
        self.label_38.setText(QCoreApplication.translate("SettingNew", u"\u5173\u95ed\u8bbe\u7f6e", None))
        self.showCloseButton0.setText(QCoreApplication.translate("SettingNew", u"\u5173\u95ed\u540e\u9000\u51fa", None))
        self.showCloseButton1.setText(QCoreApplication.translate("SettingNew", u"\u5173\u95ed\u540e\u6700\u5c0f\u5316\u5230\u6258\u76d8", None))
        self.label_2.setText(QCoreApplication.translate("SettingNew", u"\u5c01\u9762\u663e\u793a\u5927\u5c0f\uff08\u9ed8\u8ba4\u4e3a100%\uff09\uff1a", None))
        self.label_29.setText(QCoreApplication.translate("SettingNew", u"\u5206\u7c7b\u5c01\u9762\u5927\u5c0f\uff1a", None))
        self.label_44.setText(QCoreApplication.translate("SettingNew", u"\u6807\u9898\u663e\u793a\u884c\u6570", None))
        self.titleLineBox.setItemText(0, QCoreApplication.translate("SettingNew", u"\u4e0d\u663e\u793a", None))
        self.titleLineBox.setItemText(1, QCoreApplication.translate("SettingNew", u"1\u884c", None))
        self.titleLineBox.setItemText(2, QCoreApplication.translate("SettingNew", u"2\u884c", None))
        self.titleLineBox.setItemText(3, QCoreApplication.translate("SettingNew", u"3\u884c", None))
        self.titleLineBox.setItemText(4, QCoreApplication.translate("SettingNew", u"\u5168\u90e8", None))

        self.label_45.setText(QCoreApplication.translate("SettingNew", u"\u5206\u7c7b\u663e\u793a", None))
        self.categoryBox.setItemText(0, QCoreApplication.translate("SettingNew", u"\u663e\u793a", None))
        self.categoryBox.setItemText(1, QCoreApplication.translate("SettingNew", u"\u4e0d\u663e\u793a", None))

        self.label_40.setText(QCoreApplication.translate("SettingNew", u"\u56fe\u7247\u6d4f\u89c8\u8bbe\u7f6e", None))
        self.openglBox.setText(QCoreApplication.translate("SettingNew", u"\u5f00\u542fOpenGL\u52a0\u901f", None))
        self.label_10.setText(QCoreApplication.translate("SettingNew", u"\u65e5\u5fd7\u7b49\u7ea7\uff1a", None))
        self.logutton0.setText(QCoreApplication.translate("SettingNew", u"Warn", None))
        self.logutton1.setText(QCoreApplication.translate("SettingNew", u"Info", None))
        self.logutton2.setText(QCoreApplication.translate("SettingNew", u"Debug\uff08\u8be5\u8bbe\u7f6e\u5185\u542b\u654f\u611f\u6570\u636e\uff0clog\u6587\u4ef6\u8bf7\u52ff\u5206\u4eab\uff09", None))
        self.proxyLabel.setText(QCoreApplication.translate("SettingNew", u"\u4ee3\u7406", None))
        self.label_7.setText(QCoreApplication.translate("SettingNew", u"Http\u4ee3\u7406\uff1a", None))
        self.proxy0.setText(QCoreApplication.translate("SettingNew", u"\u65e0\u4ee3\u7406", None))
        self.proxy1.setText(QCoreApplication.translate("SettingNew", u"HTTP\u4ee3\u7406", None))
        self.label_31.setText(QCoreApplication.translate("SettingNew", u"\u4ee3\u7406\u5730\u5740", None))
        self.proxy2.setText(QCoreApplication.translate("SettingNew", u"Sock5\u4ee3\u7406", None))
        self.label_32.setText(QCoreApplication.translate("SettingNew", u"\u4ee3\u7406\u5730\u5740", None))
        self.proxy3.setText(QCoreApplication.translate("SettingNew", u"\u4f7f\u7528\u7cfb\u7edf\u4ee3\u7406", None))
        self.openProxy.setText(QCoreApplication.translate("SettingNew", u"\u6253\u5f00\u5206\u6d41\u8bbe\u7f6e", None))
        self.label_9.setText(QCoreApplication.translate("SettingNew", u"\u804a\u5929\u5ba4\uff1a", None))
        self.chatProxy.setText(QCoreApplication.translate("SettingNew", u"\u542f\u7528\u4ee3\u7406", None))
        self.waifu2xLabel.setText(QCoreApplication.translate("SettingNew", u"Waifu2x\u8bbe\u7f6e", None))
        self.label_20.setText(QCoreApplication.translate("SettingNew", u"CPU/GPU\u9009\u62e9\uff08\u9700\u91cd\u542f\u751f\u6548\uff09", None))
        self.label_11.setText(QCoreApplication.translate("SettingNew", u"\u4f7f\u7528CPU\u6570\u91cf\uff08CPU\u6a21\u5f0f\u751f\u6548\uff0c\u9700\u91cd\u542f\uff09", None))
        self.threadSelect.setItemText(0, QCoreApplication.translate("SettingNew", u"Auto", None))

        self.label_39.setText(QCoreApplication.translate("SettingNew", u"Tile\u5927\u5c0f\uff0c\u964d\u4f4e\u53ef\u51cf\u5c11\u663e\u5b58\u5360\u7528\uff08\u5982\u51fa\u73b0\u90e8\u5206\u56fe\u7247\u65e0\u6cd5\u8f6c\u6362\u53ef\u8c03\u4f4e\u8be5\u503c\uff09", None))
        self.tileComboBox.setItemText(0, QCoreApplication.translate("SettingNew", u"Auto", None))
        self.tileComboBox.setItemText(1, QCoreApplication.translate("SettingNew", u"200", None))
        self.tileComboBox.setItemText(2, QCoreApplication.translate("SettingNew", u"100", None))
        self.tileComboBox.setItemText(3, QCoreApplication.translate("SettingNew", u"32", None))

        self.label_12.setText(QCoreApplication.translate("SettingNew", u"Waifu2x\u770b\u56fe\u6a21\u5f0f", None))
        self.readCheckBox.setText(QCoreApplication.translate("SettingNew", u"\u662f\u5426\u542f\u7528", None))
        self.preDownWaifu2x.setText(QCoreApplication.translate("SettingNew", u"\u4f18\u5148\u4f7f\u7528\u4e0b\u8f7d\u8f6c\u6362\u597d\u7684\u7f13\u5b58", None))
        self.label_28.setText(QCoreApplication.translate("SettingNew", u"\u4e3a\u4e86\u4fdd\u8bc1\u901f\u5ea6\uff0c\u56fe\u7247\u5206\u8fa8\u7387\u5c0f\u4e8e\u7b49\u4e8e\u8be5\u503c\u65f6\u624d\u8fdb\u884c\u8f6c\u6362\uff08\u9ed8\u8ba44096P\uff09", None))
        self.label_14.setText(QCoreApplication.translate("SettingNew", u"\u6a21\u578b", None))
        self.readModelName.setText("")
        self.label_15.setText(QCoreApplication.translate("SettingNew", u"\u653e\u5927\u500d\u6570", None))
        self.label_24.setText(QCoreApplication.translate("SettingNew", u"Waifu2x\u5c01\u9762\u6a21\u5f0f\uff08\u5f00\u542f\u540e\u6240\u6709\u5c01\u9762\u4f1a\u7ecf\u8fc7Waifu2x\u5904\u7406\uff09", None))
        self.coverCheckBox.setText(QCoreApplication.translate("SettingNew", u"\u662f\u5426\u542f\u7528", None))
        self.label_22.setText(QCoreApplication.translate("SettingNew", u"\u4e3a\u4e86\u4fdd\u8bc1\u901f\u5ea6\uff0c\u5c01\u9762\u5206\u8fa8\u7387\u5c0f\u4e8e\u7b49\u4e8e\u8be5\u503c\u65f6\u624d\u8fdb\u884c\u8f6c\u6362\uff08\u9ed8\u8ba4400P\uff09", None))
        self.label_25.setText(QCoreApplication.translate("SettingNew", u"\u6a21\u578b", None))
        self.coverModelName.setText("")
        self.label_26.setText(QCoreApplication.translate("SettingNew", u"\u653e\u5927\u500d\u6570", None))
        self.label_16.setText(QCoreApplication.translate("SettingNew", u"waifu2x\u4e0b\u8f7d\u6a21\u5f0f\uff08\u5f00\u542f\u540e\u4e0b\u8f7d\u5b8c\u6210\u4f1a\u7ecf\u8fc7Waifu2x\u5904\u7406\uff09", None))
        self.downAuto.setText(QCoreApplication.translate("SettingNew", u"\u4e0b\u8f7d\u5b8c\u540e\u81ea\u52a8\u8f6c\u6362", None))
        self.label_18.setText(QCoreApplication.translate("SettingNew", u"\u6a21\u578b", None))
        self.downModelName.setText("")
        self.label_19.setText(QCoreApplication.translate("SettingNew", u"\u653e\u5927\u500d\u6570", None))
        self.downloadLabel.setText(QCoreApplication.translate("SettingNew", u"\u4e0b\u8f7d\u4e0e\u7f13\u5b58", None))
        self.label_36.setText(QCoreApplication.translate("SettingNew", u"\u4fdd\u5b58\u8def\u5f84\u683c\u5f0f\u8bbe\u7f6e\uff08\u65b0\u4e0b\u8f7d\u7684\u6587\u4ef6\u624d\u80fd\u751f\u6548\uff09", None))
        self.saveNameButton0.setText(QCoreApplication.translate("SettingNew", u"\u4f5c\u54c1\u540d\uff08\u9ed8\u8ba4\uff09", None))
        self.saveNameButton1.setText(QCoreApplication.translate("SettingNew", u"[\u4f5c\u8005\u540d]\u4f5c\u54c1\u540d", None))
        self.saveNameButton2.setText(QCoreApplication.translate("SettingNew", u"\u4f5c\u8005\u540d\u5355\u72ec\u76ee\u5f55\uff08\u5982\u65e0\u4f5c\u8005\u540d\u5c06\u653e\u5165default\u76ee\u5f55\uff09", None))
        self.label_21.setText(QCoreApplication.translate("SettingNew", u"\u4e0b\u8f7d\u548c\u7f13\u5b58\u8def\u5f84\uff08\u7f13\u5b58\u6587\u4ef6\u9700\u81ea\u5df1\u624b\u52a8\u6e05\u9664\uff09", None))
        self.setDirButton.setText(QCoreApplication.translate("SettingNew", u"\u8bbe\u7f6e\u76ee\u5f55", None))
        self.setLogDirButton.setText(QCoreApplication.translate("SettingNew", u"\u8bbe\u7f6e\u65e5\u5fd7\u76ee\u5f55", None))
        self.label_3.setText(QCoreApplication.translate("SettingNew", u"\u4e0b\u8f7d", None))
        self.downloadDir.setText("")
        self.openDownloadDir.setText(QCoreApplication.translate("SettingNew", u"\u6253\u5f00\u76ee\u5f55", None))
        self.label_4.setText(QCoreApplication.translate("SettingNew", u"\u7f13\u5b58", None))
        self.cacheDir.setText("")
        self.openCacheDir.setText(QCoreApplication.translate("SettingNew", u"\u6253\u5f00\u76ee\u5f55", None))
        self.label_27.setText(QCoreApplication.translate("SettingNew", u"\u804a\u5929\u7f13\u5b58", None))
        self.chatDir.setText("")
        self.openChatDir.setText(QCoreApplication.translate("SettingNew", u"\u6253\u5f00\u76ee\u5f55", None))
        self.label_5.setText(QCoreApplication.translate("SettingNew", u"Waifu2x\u7f13\u5b58", None))
        self.waifu2xDir.setText("")
        self.openWaifu2xDir.setText(QCoreApplication.translate("SettingNew", u"\u6253\u5f00\u76ee\u5f55", None))
        self.label_42.setText(QCoreApplication.translate("SettingNew", u"\u65e5\u5fd7", None))
        self.logLabel.setText("")
        self.openLogDir.setText(QCoreApplication.translate("SettingNew", u"\u6253\u5f00\u76ee\u5f55", None))
    # retranslateUi

