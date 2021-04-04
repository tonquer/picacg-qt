# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Setting(object):
    def setupUi(self, Setting):
        if not Setting.objectName():
            Setting.setObjectName(u"Setting")
        Setting.resize(482, 382)
        self.gridLayout_2 = QGridLayout(Setting)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(Setting)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.NoFrame)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.encodeSelect = QComboBox(Setting)
        self.encodeSelect.setObjectName(u"encodeSelect")

        self.gridLayout_3.addWidget(self.encodeSelect, 7, 2, 1, 1)

        self.checkBox = QCheckBox(Setting)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_3.addWidget(self.checkBox, 5, 2, 1, 1)

        self.label_3 = QLabel(Setting)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 7, 0, 1, 1)

        self.label_11 = QLabel(Setting)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_3.addWidget(self.label_11, 9, 0, 1, 1)

        self.checkBox_2 = QCheckBox(Setting)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setChecked(True)

        self.gridLayout_3.addWidget(self.checkBox_2, 2, 2, 1, 1)

        self.label_4 = QLabel(Setting)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_7 = QLabel(Setting)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 10, 0, 1, 1)

        self.label_8 = QLabel(Setting)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 8, 0, 1, 1)

        self.lookModel = QComboBox(Setting)
        self.lookModel.addItem("")
        self.lookModel.addItem("")
        self.lookModel.addItem("")
        self.lookModel.addItem("")
        self.lookModel.setObjectName(u"lookModel")

        self.gridLayout_3.addWidget(self.lookModel, 9, 2, 1, 1)

        self.threadSelect = QComboBox(Setting)
        self.threadSelect.addItem("")
        self.threadSelect.setObjectName(u"threadSelect")

        self.gridLayout_3.addWidget(self.threadSelect, 8, 2, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.saveEdit = QLineEdit(Setting)
        self.saveEdit.setObjectName(u"saveEdit")

        self.horizontalLayout_4.addWidget(self.saveEdit)

        self.pushButton = QPushButton(Setting)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_4.addWidget(self.pushButton)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 4, 2, 1, 1)

        self.downloadModel = QComboBox(Setting)
        self.downloadModel.addItem("")
        self.downloadModel.addItem("")
        self.downloadModel.addItem("")
        self.downloadModel.addItem("")
        self.downloadModel.setObjectName(u"downloadModel")

        self.gridLayout_3.addWidget(self.downloadModel, 10, 2, 1, 1)

        self.label_6 = QLabel(Setting)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 5, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.quality_original = QRadioButton(Setting)
        self.buttonGroup = QButtonGroup(Setting)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.quality_original)
        self.quality_original.setObjectName(u"quality_original")

        self.horizontalLayout.addWidget(self.quality_original)

        self.quality_high = QRadioButton(Setting)
        self.buttonGroup.addButton(self.quality_high)
        self.quality_high.setObjectName(u"quality_high")

        self.horizontalLayout.addWidget(self.quality_high)

        self.quality_medium = QRadioButton(Setting)
        self.buttonGroup.addButton(self.quality_medium)
        self.quality_medium.setObjectName(u"quality_medium")

        self.horizontalLayout.addWidget(self.quality_medium)

        self.quality_low = QRadioButton(Setting)
        self.buttonGroup.addButton(self.quality_low)
        self.quality_low.setObjectName(u"quality_low")

        self.horizontalLayout.addWidget(self.quality_low)


        self.gridLayout_3.addLayout(self.horizontalLayout, 3, 2, 1, 1)

        self.httpEdit = QLineEdit(Setting)
        self.httpEdit.setObjectName(u"httpEdit")

        self.gridLayout_3.addWidget(self.httpEdit, 1, 2, 1, 1)

        self.label_9 = QLabel(Setting)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 2, 0, 1, 1)

        self.comboBox = QComboBox(Setting)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_3.addWidget(self.comboBox, 0, 2, 1, 1)

        self.label_2 = QLabel(Setting)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_5 = QLabel(Setting)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 4, 0, 1, 1)

        self.logBox = QComboBox(Setting)
        self.logBox.addItem("")
        self.logBox.addItem("")
        self.logBox.addItem("")
        self.logBox.setObjectName(u"logBox")

        self.gridLayout_3.addWidget(self.logBox, 6, 2, 1, 1)

        self.label_10 = QLabel(Setting)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 6, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Setting)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Setting)
        self.buttonBox.accepted.connect(Setting.SaveSetting)
        self.buttonBox.rejected.connect(Setting.close)
        self.pushButton.clicked.connect(Setting.SelectSavePath)

        QMetaObject.connectSlotsByName(Setting)
    # setupUi

    def retranslateUi(self, Setting):
        Setting.setWindowTitle(QCoreApplication.translate("Setting", u"Form", None))
        self.label.setText(QCoreApplication.translate("Setting", u"\u4e0b\u8f7d\u7ebf\u7a0b\u6570", None))
        self.checkBox.setText(QCoreApplication.translate("Setting", u"\u662f\u5426\u542f\u7528", None))
        self.label_3.setText(QCoreApplication.translate("Setting", u"\u89e3\u7801\u5668\uff08\u9700\u91cd\u542f\uff09", None))
        self.label_11.setText(QCoreApplication.translate("Setting", u"\u770b\u56fe\u65f6\u6a21\u578b", None))
        self.checkBox_2.setText(QCoreApplication.translate("Setting", u"\u542f\u7528\u4ee3\u7406", None))
        self.label_4.setText(QCoreApplication.translate("Setting", u"\u753b\u8d28\u9009\u62e9", None))
        self.label_7.setText(QCoreApplication.translate("Setting", u"\u4e0b\u8f7d\u65f6\u6a21\u578b", None))
        self.label_8.setText(QCoreApplication.translate("Setting", u"\u7ebf\u7a0b\u6570", None))
        self.lookModel.setItemText(0, QCoreApplication.translate("Setting", u"\u81ea\u52a8", None))
        self.lookModel.setItemText(1, QCoreApplication.translate("Setting", u"cunet\uff08\u6548\u679c\u6700\u597d\uff09", None))
        self.lookModel.setItemText(2, QCoreApplication.translate("Setting", u"photo\uff08\u5199\u771f\uff09\uff08\u901f\u5ea6\u5feb\uff09", None))
        self.lookModel.setItemText(3, QCoreApplication.translate("Setting", u"anime_style_art_rgb\uff08\u52a8\u6f2b\uff09\uff08\u901f\u5ea6\u5feb\uff09", None))

        self.threadSelect.setItemText(0, QCoreApplication.translate("Setting", u"2", None))

        self.pushButton.setText(QCoreApplication.translate("Setting", u"...", None))
        self.downloadModel.setItemText(0, QCoreApplication.translate("Setting", u"\u81ea\u52a8", None))
        self.downloadModel.setItemText(1, QCoreApplication.translate("Setting", u"cunet\uff08\u6548\u679c\u597d\uff09", None))
        self.downloadModel.setItemText(2, QCoreApplication.translate("Setting", u"photo\uff08\u5199\u771f\uff09\uff08\u901f\u5ea6\u5feb\uff09", None))
        self.downloadModel.setItemText(3, QCoreApplication.translate("Setting", u"anime_style_art_rgb\uff08\u52a8\u6f2b\uff09\uff08\u901f\u5ea6\u5feb\uff09", None))

        self.label_6.setText(QCoreApplication.translate("Setting", u"waifu2x\u8bbe\u7f6e", None))
        self.quality_original.setText(QCoreApplication.translate("Setting", u"\u539f\u753b", None))
        self.quality_high.setText(QCoreApplication.translate("Setting", u"\u9ad8", None))
        self.quality_medium.setText(QCoreApplication.translate("Setting", u"\u4e2d", None))
        self.quality_low.setText(QCoreApplication.translate("Setting", u"\u4f4e", None))
        self.httpEdit.setPlaceholderText(QCoreApplication.translate("Setting", u"http://127.0.0.1:10809", None))
        self.label_9.setText(QCoreApplication.translate("Setting", u"\u804a\u5929\u5ba4", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Setting", u"2", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Setting", u"3", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Setting", u"4", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Setting", u"5", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Setting", u"6", None))

        self.comboBox.setPlaceholderText("")
        self.label_2.setText(QCoreApplication.translate("Setting", u"http\u4ee3\u7406", None))
        self.label_5.setText(QCoreApplication.translate("Setting", u"\u4fdd\u5b58\u8def\u5f84", None))
        self.logBox.setItemText(0, QCoreApplication.translate("Setting", u"WARN", None))
        self.logBox.setItemText(1, QCoreApplication.translate("Setting", u"INFO", None))
        self.logBox.setItemText(2, QCoreApplication.translate("Setting", u"DEBUG", None))

        self.label_10.setText(QCoreApplication.translate("Setting", u"\u65e5\u5fd7\u7b49\u7ea7", None))
    # retranslateUi

