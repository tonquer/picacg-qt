# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_setting.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

from component.box.wheel_combo_box import WheelComboBox
from component.box.wheel_double_spin_box import WheelDoubleSpinBox
from component.box.wheel_spin_box import WheelSpinBox
from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_Setting(object):
    def setupUi(self, Setting):
        if not Setting.objectName():
            Setting.setObjectName(u"Setting")
        Setting.resize(494, 649)
        Setting.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(Setting)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = SmoothScrollArea(Setting)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 474, 629))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.line_9 = QFrame(self.scrollAreaWidgetContents)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.VLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_9, 0, 1, 1, 1)

        self.label_update = QLabel(self.scrollAreaWidgetContents)
        self.label_update.setObjectName(u"label_update")
        self.label_update.setMaximumSize(QSize(16777215, 19))

        self.gridLayout_5.addWidget(self.label_update, 2, 0, 1, 1)

        self.encodeSelect = QComboBox(self.scrollAreaWidgetContents)
        self.encodeSelect.setObjectName(u"encodeSelect")

        self.gridLayout_5.addWidget(self.encodeSelect, 12, 2, 1, 1)

        self.line_18 = QFrame(self.scrollAreaWidgetContents)
        self.line_18.setObjectName(u"line_18")
        self.line_18.setFrameShape(QFrame.VLine)
        self.line_18.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_18, 12, 1, 1, 1)

        self.line_8 = QFrame(self.scrollAreaWidgetContents)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_8, 9, 2, 1, 1)

        self.line_10 = QFrame(self.scrollAreaWidgetContents)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.VLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_10, 2, 1, 1, 1)

        self.checkBox = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_5.addWidget(self.checkBox, 10, 2, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 26))

        self.gridLayout_5.addWidget(self.label_2, 5, 0, 1, 1)

        self.langSelect = WheelComboBox(self.scrollAreaWidgetContents)
        self.langSelect.addItem("")
        self.langSelect.addItem("")
        self.langSelect.addItem("")
        self.langSelect.setObjectName(u"langSelect")

        self.gridLayout_5.addWidget(self.langSelect, 3, 2, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(16777215, 19))

        self.gridLayout_5.addWidget(self.label_6, 10, 0, 1, 1)

        self.line_14 = QFrame(self.scrollAreaWidgetContents)
        self.line_14.setObjectName(u"line_14")
        self.line_14.setFrameShape(QFrame.VLine)
        self.line_14.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_14, 7, 1, 1, 1)

        self.chatProxy = QCheckBox(self.scrollAreaWidgetContents)
        self.chatProxy.setObjectName(u"chatProxy")
        self.chatProxy.setChecked(False)

        self.gridLayout_5.addWidget(self.chatProxy, 6, 2, 1, 1)

        self.line_20 = QFrame(self.scrollAreaWidgetContents)
        self.line_20.setObjectName(u"line_20")
        self.line_20.setFrameShape(QFrame.VLine)
        self.line_20.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_20, 16, 1, 1, 1)

        self.line_17 = QFrame(self.scrollAreaWidgetContents)
        self.line_17.setObjectName(u"line_17")
        self.line_17.setFrameShape(QFrame.VLine)
        self.line_17.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_17, 11, 1, 1, 1)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line, 15, 0, 1, 1)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 21))
        self.label.setFrameShape(QFrame.NoFrame)

        self.gridLayout_5.addWidget(self.label, 4, 0, 1, 1)

        self.comboBox = WheelComboBox(self.scrollAreaWidgetContents)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_5.addWidget(self.comboBox, 4, 2, 1, 1)

        self.line_19 = QFrame(self.scrollAreaWidgetContents)
        self.line_19.setObjectName(u"line_19")
        self.line_19.setFrameShape(QFrame.VLine)
        self.line_19.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_19, 14, 1, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line_4, 0, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.readNoise = WheelComboBox(self.scrollAreaWidgetContents)
        self.readNoise.addItem("")
        self.readNoise.addItem("")
        self.readNoise.addItem("")
        self.readNoise.addItem("")
        self.readNoise.addItem("")
        self.readNoise.setObjectName(u"readNoise")

        self.gridLayout_4.addWidget(self.readNoise, 0, 2, 1, 1)

        self.label_13 = QLabel(self.scrollAreaWidgetContents)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMaximumSize(QSize(156, 16777215))

        self.gridLayout_4.addWidget(self.label_13, 0, 0, 1, 1)

        self.readModel = WheelComboBox(self.scrollAreaWidgetContents)
        self.readModel.addItem("")
        self.readModel.addItem("")
        self.readModel.addItem("")
        self.readModel.addItem("")
        self.readModel.setObjectName(u"readModel")

        self.gridLayout_4.addWidget(self.readModel, 1, 2, 1, 1)

        self.label_15 = QLabel(self.scrollAreaWidgetContents)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMaximumSize(QSize(156, 16777215))

        self.gridLayout_4.addWidget(self.label_15, 2, 0, 1, 1)

        self.label_14 = QLabel(self.scrollAreaWidgetContents)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(156, 16777215))

        self.gridLayout_4.addWidget(self.label_14, 1, 0, 1, 1)

        self.readScale = WheelDoubleSpinBox(self.scrollAreaWidgetContents)
        self.readScale.setObjectName(u"readScale")
        self.readScale.setDecimals(1)
        self.readScale.setMaximum(32.000000000000000)
        self.readScale.setSingleStep(0.100000000000000)
        self.readScale.setValue(2.000000000000000)

        self.gridLayout_4.addWidget(self.readScale, 2, 2, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_4, 1, 0, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_3, 13, 2, 2, 1)

        self.line_12 = QFrame(self.scrollAreaWidgetContents)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShape(QFrame.VLine)
        self.line_12.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_12, 5, 1, 1, 1)

        self.label_lang = QLabel(self.scrollAreaWidgetContents)
        self.label_lang.setObjectName(u"label_lang")

        self.gridLayout_5.addWidget(self.label_lang, 3, 0, 1, 1)

        self.line_22 = QFrame(self.scrollAreaWidgetContents)
        self.line_22.setObjectName(u"line_22")
        self.line_22.setFrameShape(QFrame.VLine)
        self.line_22.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_22, 3, 1, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_5.addWidget(self.label_7, 7, 0, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(16777215, 19))

        self.gridLayout_5.addWidget(self.label_9, 6, 0, 1, 1)

        self.preDownNum = WheelSpinBox(self.scrollAreaWidgetContents)
        self.preDownNum.setObjectName(u"preDownNum")
        self.preDownNum.setFocusPolicy(Qt.StrongFocus)
        self.preDownNum.setMinimum(1)
        self.preDownNum.setValue(10)

        self.gridLayout_5.addWidget(self.preDownNum, 7, 2, 1, 1)

        self.line_21 = QFrame(self.scrollAreaWidgetContents)
        self.line_21.setObjectName(u"line_21")
        self.line_21.setFrameShape(QFrame.VLine)
        self.line_21.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_21, 18, 1, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_2, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_17 = QLabel(self.scrollAreaWidgetContents)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMaximumSize(QSize(156, 16777215))

        self.gridLayout.addWidget(self.label_17, 0, 0, 1, 1)

        self.downModel = WheelComboBox(self.scrollAreaWidgetContents)
        self.downModel.addItem("")
        self.downModel.addItem("")
        self.downModel.addItem("")
        self.downModel.addItem("")
        self.downModel.setObjectName(u"downModel")

        self.gridLayout.addWidget(self.downModel, 1, 1, 1, 1)

        self.label_19 = QLabel(self.scrollAreaWidgetContents)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMaximumSize(QSize(156, 16777215))

        self.gridLayout.addWidget(self.label_19, 2, 0, 1, 1)

        self.label_18 = QLabel(self.scrollAreaWidgetContents)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMaximumSize(QSize(156, 16777215))

        self.gridLayout.addWidget(self.label_18, 1, 0, 1, 1)

        self.downScale = WheelDoubleSpinBox(self.scrollAreaWidgetContents)
        self.downScale.setObjectName(u"downScale")
        self.downScale.setDecimals(1)
        self.downScale.setMaximum(32.000000000000000)
        self.downScale.setSingleStep(0.100000000000000)
        self.downScale.setValue(2.000000000000000)

        self.gridLayout.addWidget(self.downScale, 2, 1, 1, 1)

        self.downNoise = WheelComboBox(self.scrollAreaWidgetContents)
        self.downNoise.addItem("")
        self.downNoise.addItem("")
        self.downNoise.addItem("")
        self.downNoise.addItem("")
        self.downNoise.addItem("")
        self.downNoise.setObjectName(u"downNoise")

        self.gridLayout.addWidget(self.downNoise, 0, 1, 1, 1)

        self.downAuto = QCheckBox(self.scrollAreaWidgetContents)
        self.downAuto.setObjectName(u"downAuto")
        self.downAuto.setChecked(True)

        self.gridLayout.addWidget(self.downAuto, 3, 0, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_2, 15, 2, 2, 1)

        self.checkBox_IsUpdate = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_IsUpdate.setObjectName(u"checkBox_IsUpdate")

        self.gridLayout_5.addWidget(self.checkBox_IsUpdate, 2, 2, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.saveEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.saveEdit.setObjectName(u"saveEdit")

        self.horizontalLayout_4.addWidget(self.saveEdit)

        self.pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_4.addWidget(self.pushButton)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)


        self.gridLayout_5.addLayout(self.horizontalLayout_3, 8, 2, 1, 1)

        self.label_12 = QLabel(self.scrollAreaWidgetContents)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMaximumSize(QSize(16777215, 84))

        self.gridLayout_5.addWidget(self.label_12, 14, 0, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 21))

        self.gridLayout_5.addWidget(self.label_3, 12, 0, 1, 1)

        self.line_16 = QFrame(self.scrollAreaWidgetContents)
        self.line_16.setObjectName(u"line_16")
        self.line_16.setFrameShape(QFrame.VLine)
        self.line_16.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_16, 10, 1, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(16777215, 21))

        self.gridLayout_5.addWidget(self.label_8, 11, 0, 1, 1)

        self.threadSelect = WheelComboBox(self.scrollAreaWidgetContents)
        self.threadSelect.addItem("")
        self.threadSelect.setObjectName(u"threadSelect")
        self.threadSelect.setFocusPolicy(Qt.StrongFocus)

        self.gridLayout_5.addWidget(self.threadSelect, 11, 2, 1, 1)

        self.line_15 = QFrame(self.scrollAreaWidgetContents)
        self.line_15.setObjectName(u"line_15")
        self.line_15.setFrameShape(QFrame.VLine)
        self.line_15.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_15, 8, 1, 1, 1)

        self.line_6 = QFrame(self.scrollAreaWidgetContents)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_6, 17, 2, 1, 1)

        self.line_7 = QFrame(self.scrollAreaWidgetContents)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_7, 9, 0, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 32))

        self.gridLayout_5.addWidget(self.label_5, 8, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.httpProxy = QCheckBox(self.scrollAreaWidgetContents)
        self.httpProxy.setObjectName(u"httpProxy")

        self.horizontalLayout_5.addWidget(self.httpProxy)

        self.httpEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.httpEdit.setObjectName(u"httpEdit")

        self.horizontalLayout_5.addWidget(self.httpEdit)

        self.toolButton = QToolButton(self.scrollAreaWidgetContents)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setCheckable(False)

        self.horizontalLayout_5.addWidget(self.toolButton)


        self.gridLayout_5.addLayout(self.horizontalLayout_5, 5, 2, 1, 1)

        self.line_11 = QFrame(self.scrollAreaWidgetContents)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.VLine)
        self.line_11.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_11, 4, 1, 1, 1)

        self.logBox = WheelComboBox(self.scrollAreaWidgetContents)
        self.logBox.addItem("")
        self.logBox.addItem("")
        self.logBox.addItem("")
        self.logBox.setObjectName(u"logBox")
        self.logBox.setFocusPolicy(Qt.StrongFocus)

        self.gridLayout_5.addWidget(self.logBox, 18, 2, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 21))

        self.gridLayout_5.addWidget(self.label_4, 0, 0, 1, 1)

        self.line_3 = QFrame(self.scrollAreaWidgetContents)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_3, 13, 0, 1, 1)

        self.label_16 = QLabel(self.scrollAreaWidgetContents)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMaximumSize(QSize(16777215, 110))

        self.gridLayout_5.addWidget(self.label_16, 16, 0, 1, 1)

        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(16777215, 21))

        self.gridLayout_5.addWidget(self.label_10, 18, 0, 1, 1)

        self.line_5 = QFrame(self.scrollAreaWidgetContents)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_5, 17, 0, 1, 1)

        self.line_13 = QFrame(self.scrollAreaWidgetContents)
        self.line_13.setObjectName(u"line_13")
        self.line_13.setFrameShape(QFrame.VLine)
        self.line_13.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_13, 6, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.themeButton2 = QRadioButton(self.scrollAreaWidgetContents)
        self.themeGroup = QButtonGroup(Setting)
        self.themeGroup.setObjectName(u"themeGroup")
        self.themeGroup.addButton(self.themeButton2)
        self.themeButton2.setObjectName(u"themeButton2")

        self.horizontalLayout.addWidget(self.themeButton2)

        self.themeButton1 = QRadioButton(self.scrollAreaWidgetContents)
        self.themeGroup.addButton(self.themeButton1)
        self.themeButton1.setObjectName(u"themeButton1")

        self.horizontalLayout.addWidget(self.themeButton1)

        self.themeButton0 = QRadioButton(self.scrollAreaWidgetContents)
        self.themeGroup.addButton(self.themeButton0)
        self.themeButton0.setObjectName(u"themeButton0")
        self.themeButton0.setChecked(True)

        self.horizontalLayout.addWidget(self.themeButton0)


        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_5)

        self.saveButton = QPushButton(self.scrollAreaWidgetContents)
        self.saveButton.setObjectName(u"saveButton")

        self.verticalLayout_2.addWidget(self.saveButton)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Setting)
        self.pushButton.clicked.connect(Setting.SelectSavePath)
        self.saveButton.clicked.connect(Setting.SaveSetting)

        QMetaObject.connectSlotsByName(Setting)
    # setupUi

    def retranslateUi(self, Setting):
        Setting.setWindowTitle(QCoreApplication.translate("Setting", u"\u8bbe\u7f6e", None))
        self.label_update.setText(QCoreApplication.translate("Setting", u"\u66f4\u65b0", None))
        self.checkBox.setText(QCoreApplication.translate("Setting", u"\u662f\u5426\u542f\u7528", None))
        self.label_2.setText(QCoreApplication.translate("Setting", u"http\u4ee3\u7406", None))
        self.langSelect.setItemText(0, QCoreApplication.translate("Setting", u"Chinese-Simplified", None))
        self.langSelect.setItemText(1, QCoreApplication.translate("Setting", u"Chinese-Traditional", None))
        self.langSelect.setItemText(2, QCoreApplication.translate("Setting", u"English", None))

        self.label_6.setText(QCoreApplication.translate("Setting", u"waifu2x\u8bbe\u7f6e", None))
        self.chatProxy.setText(QCoreApplication.translate("Setting", u"\u542f\u7528\u4ee3\u7406", None))
        self.label.setText(QCoreApplication.translate("Setting", u"\u4e0b\u8f7d\u7ebf\u7a0b\u6570", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Setting", u"2", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Setting", u"3", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Setting", u"4", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Setting", u"5", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Setting", u"6", None))

        self.comboBox.setPlaceholderText("")
        self.readNoise.setItemText(0, QCoreApplication.translate("Setting", u"\u81ea\u52a8", None))
        self.readNoise.setItemText(1, QCoreApplication.translate("Setting", u"0", None))
        self.readNoise.setItemText(2, QCoreApplication.translate("Setting", u"1", None))
        self.readNoise.setItemText(3, QCoreApplication.translate("Setting", u"2", None))
        self.readNoise.setItemText(4, QCoreApplication.translate("Setting", u"3", None))

        self.label_13.setText(QCoreApplication.translate("Setting", u"\u53bb\u566a\u7b49\u7ea7", None))
        self.readModel.setItemText(0, QCoreApplication.translate("Setting", u"\u81ea\u52a8", None))
        self.readModel.setItemText(1, QCoreApplication.translate("Setting", u"cunet", None))
        self.readModel.setItemText(2, QCoreApplication.translate("Setting", u"photo", None))
        self.readModel.setItemText(3, QCoreApplication.translate("Setting", u"anime_style_art_rgb", None))

        self.label_15.setText(QCoreApplication.translate("Setting", u"\u653e\u5927\u500d\u6570", None))
        self.label_14.setText(QCoreApplication.translate("Setting", u"\u6a21\u578b", None))
        self.label_lang.setText(QCoreApplication.translate("Setting", u"\u8bed\u8a00", None))
        self.label_7.setText(QCoreApplication.translate("Setting", u"\u770b\u56fe\u9884\u52a0\u8f7d\u6570", None))
        self.label_9.setText(QCoreApplication.translate("Setting", u"\u804a\u5929\u5ba4", None))
        self.label_17.setText(QCoreApplication.translate("Setting", u"\u53bb\u566a\u7b49\u7ea7", None))
        self.downModel.setItemText(0, QCoreApplication.translate("Setting", u"\u81ea\u52a8", None))
        self.downModel.setItemText(1, QCoreApplication.translate("Setting", u"cunet", None))
        self.downModel.setItemText(2, QCoreApplication.translate("Setting", u"photo", None))
        self.downModel.setItemText(3, QCoreApplication.translate("Setting", u"anime_style_art_rgb", None))

        self.label_19.setText(QCoreApplication.translate("Setting", u"\u653e\u5927\u500d\u6570", None))
        self.label_18.setText(QCoreApplication.translate("Setting", u"\u6a21\u578b", None))
        self.downNoise.setItemText(0, QCoreApplication.translate("Setting", u"\u81ea\u52a8", None))
        self.downNoise.setItemText(1, QCoreApplication.translate("Setting", u"0", None))
        self.downNoise.setItemText(2, QCoreApplication.translate("Setting", u"1", None))
        self.downNoise.setItemText(3, QCoreApplication.translate("Setting", u"2", None))
        self.downNoise.setItemText(4, QCoreApplication.translate("Setting", u"3", None))

        self.downAuto.setText(QCoreApplication.translate("Setting", u"\u4e0b\u8f7d\u5b8c\u540e\u81ea\u52a8\u8f6c\u6362", None))
        self.checkBox_IsUpdate.setText(QCoreApplication.translate("Setting", u"\u542f\u52a8\u65f6\u68c0\u67e5\u66f4\u65b0", None))
        self.pushButton.setText(QCoreApplication.translate("Setting", u"...", None))
        self.label_12.setText(QCoreApplication.translate("Setting", u"Waifu2x\u770b\u56fe\u6a21\u5f0f", None))
        self.label_3.setText(QCoreApplication.translate("Setting", u"\u89e3\u7801\u5668\uff08\u9700\u91cd\u542f\uff09", None))
        self.label_8.setText(QCoreApplication.translate("Setting", u"waifu2x\u7ebf\u7a0b\u6570", None))
        self.threadSelect.setItemText(0, QCoreApplication.translate("Setting", u"2", None))

        self.label_5.setText(QCoreApplication.translate("Setting", u"\u4e0b\u8f7d\u548c\u7f13\u5b58\u8def\u5f84", None))
#if QT_CONFIG(tooltip)
        self.httpProxy.setToolTip(QCoreApplication.translate("Setting", u"<html><head/><body><p>\u8bf7\u586b\u5199\u4f60\u7684\u4ee3\u7406\u8f6f\u4ef6\u63d0\u4f9b\u7684\u4ee3\u7406\u5730\u5740</p><p>\u5982:</p><p>v2ray\u53ef\u80fd\u662f http://127.0.0.1:10809</p><p>shadowsocks\u53ef\u80fd\u662f http://127.0.0.1:1080</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.httpProxy.setText(QCoreApplication.translate("Setting", u"\u542f\u7528\u4ee3\u7406", None))
#if QT_CONFIG(tooltip)
        self.httpEdit.setToolTip(QCoreApplication.translate("Setting", u"<html><head/><body><p>\u8bf7\u586b\u5199\u4f60\u7684\u4ee3\u7406\u8f6f\u4ef6\u63d0\u4f9b\u7684\u4ee3\u7406\u5730\u5740</p><p>\u5982:</p><p>v2ray\u53ef\u80fd\u662f http://127.0.0.1:10809</p><p>shadowsocks\u53ef\u80fd\u662f http://127.0.0.1:1080</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.httpEdit.setPlaceholderText("")
#if QT_CONFIG(tooltip)
        self.toolButton.setToolTip(QCoreApplication.translate("Setting", u"<html><head/><body><p>\u8bf7\u586b\u5199\u4f60\u7684\u4ee3\u7406\u8f6f\u4ef6\u63d0\u4f9b\u7684\u4ee3\u7406\u5730\u5740</p><p>\u5982:</p><p>v2ray\u53ef\u80fd\u662f http://127.0.0.1:10809</p><p>shadowsocks\u53ef\u80fd\u662f http://127.0.0.1:1080</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton.setText(QCoreApplication.translate("Setting", u"?", None))
        self.logBox.setItemText(0, QCoreApplication.translate("Setting", u"WARN", None))
        self.logBox.setItemText(1, QCoreApplication.translate("Setting", u"INFO", None))
        self.logBox.setItemText(2, QCoreApplication.translate("Setting", u"DEBUG", None))

        self.label_4.setText(QCoreApplication.translate("Setting", u"\u4e3b\u9898", None))
        self.label_16.setText(QCoreApplication.translate("Setting", u"waifu2x\u4e0b\u8f7d\u6a21\u5f0f", None))
        self.label_10.setText(QCoreApplication.translate("Setting", u"\u65e5\u5fd7\u7b49\u7ea7", None))
        self.themeButton2.setText(QCoreApplication.translate("Setting", u"\u767d", None))
        self.themeButton1.setText(QCoreApplication.translate("Setting", u"\u9ed1", None))
        self.themeButton0.setText(QCoreApplication.translate("Setting", u"\u8ddf\u968f\u7cfb\u7edf", None))
        self.saveButton.setText(QCoreApplication.translate("Setting", u"\u4fdd\u5b58\u8bbe\u7f6e", None))
    # retranslateUi

