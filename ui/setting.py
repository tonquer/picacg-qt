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
        Setting.resize(482, 364)
        self.gridLayout_2 = QGridLayout(Setting)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_5 = QLabel(Setting)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_8 = QLabel(Setting)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 6, 0, 1, 1)

        self.label_11 = QLabel(Setting)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_3.addWidget(self.label_11, 9, 0, 1, 1)

        self.label_3 = QLabel(Setting)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 5, 0, 1, 1)

        self.encodeSelect = QComboBox(Setting)
        self.encodeSelect.setObjectName(u"encodeSelect")

        self.gridLayout_3.addWidget(self.encodeSelect, 5, 2, 1, 1)

        self.httpEdit = QLineEdit(Setting)
        self.httpEdit.setObjectName(u"httpEdit")

        self.gridLayout_3.addWidget(self.httpEdit, 1, 2, 1, 1)

        self.scaleSelect = QComboBox(Setting)
        self.scaleSelect.addItem("")
        self.scaleSelect.setObjectName(u"scaleSelect")

        self.gridLayout_3.addWidget(self.scaleSelect, 7, 2, 1, 1)

        self.label_2 = QLabel(Setting)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_4 = QLabel(Setting)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_9 = QLabel(Setting)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 7, 0, 1, 1)

        self.threadSelect = QComboBox(Setting)
        self.threadSelect.addItem("")
        self.threadSelect.setObjectName(u"threadSelect")

        self.gridLayout_3.addWidget(self.threadSelect, 6, 2, 1, 1)

        self.noiseSelect = QComboBox(Setting)
        self.noiseSelect.addItem("")
        self.noiseSelect.addItem("")
        self.noiseSelect.addItem("")
        self.noiseSelect.setObjectName(u"noiseSelect")

        self.gridLayout_3.addWidget(self.noiseSelect, 8, 2, 1, 1)

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


        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 2, 1, 1)

        self.label_6 = QLabel(Setting)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 4, 0, 1, 1)

        self.label_10 = QLabel(Setting)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 8, 0, 1, 1)

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


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 3, 2, 1, 1)

        self.label = QLabel(Setting)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.NoFrame)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.modelSelect = QComboBox(Setting)
        self.modelSelect.addItem("")
        self.modelSelect.setObjectName(u"modelSelect")

        self.gridLayout_3.addWidget(self.modelSelect, 9, 2, 1, 1)

        self.comboBox = QComboBox(Setting)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_3.addWidget(self.comboBox, 0, 2, 1, 1)

        self.checkBox = QCheckBox(Setting)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_3.addWidget(self.checkBox, 4, 2, 1, 1)


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

        self.noiseSelect.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Setting)
    # setupUi

    def retranslateUi(self, Setting):
        Setting.setWindowTitle(QCoreApplication.translate("Setting", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("Setting", u"\u4fdd\u5b58\u8def\u5f84", None))
        self.label_8.setText(QCoreApplication.translate("Setting", u"\u7ebf\u7a0b\u6570", None))
        self.label_11.setText(QCoreApplication.translate("Setting", u"\u6a21\u578b", None))
        self.label_3.setText(QCoreApplication.translate("Setting", u"\u89e3\u7801\u5668\uff08\u9700\u91cd\u542f\uff09", None))
        self.httpEdit.setPlaceholderText(QCoreApplication.translate("Setting", u"http://127.0.0.1:10809", None))
        self.scaleSelect.setItemText(0, QCoreApplication.translate("Setting", u"2\u500d", None))

        self.label_2.setText(QCoreApplication.translate("Setting", u"http\u4ee3\u7406", None))
        self.label_4.setText(QCoreApplication.translate("Setting", u"\u753b\u8d28\u9009\u62e9", None))
        self.label_9.setText(QCoreApplication.translate("Setting", u"\u7f29\u653e\u5927\u5c0f", None))
        self.threadSelect.setItemText(0, QCoreApplication.translate("Setting", u"2", None))

        self.noiseSelect.setItemText(0, QCoreApplication.translate("Setting", u"3\uff08\u6700\u4f73\u53bb\u566a\uff09", None))
        self.noiseSelect.setItemText(1, QCoreApplication.translate("Setting", u"2", None))
        self.noiseSelect.setItemText(2, QCoreApplication.translate("Setting", u"1", None))

        self.quality_original.setText(QCoreApplication.translate("Setting", u"\u539f\u753b", None))
        self.quality_high.setText(QCoreApplication.translate("Setting", u"\u9ad8", None))
        self.quality_medium.setText(QCoreApplication.translate("Setting", u"\u4e2d", None))
        self.quality_low.setText(QCoreApplication.translate("Setting", u"\u4f4e", None))
        self.label_6.setText(QCoreApplication.translate("Setting", u"waifu2x\u8bbe\u7f6e", None))
        self.label_10.setText(QCoreApplication.translate("Setting", u"\u53bb\u566a\u7b49\u7ea7", None))
        self.pushButton.setText(QCoreApplication.translate("Setting", u"...", None))
        self.label.setText(QCoreApplication.translate("Setting", u"\u4e0b\u8f7d\u7ebf\u7a0b\u6570", None))
        self.modelSelect.setItemText(0, QCoreApplication.translate("Setting", u"models-cunet", None))

        self.comboBox.setItemText(0, QCoreApplication.translate("Setting", u"2", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Setting", u"3", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Setting", u"4", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Setting", u"5", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Setting", u"6", None))

        self.comboBox.setPlaceholderText("")
        self.checkBox.setText(QCoreApplication.translate("Setting", u"\u662f\u5426\u542f\u7528", None))
    # retranslateUi

