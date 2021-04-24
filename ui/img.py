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
        Img.resize(728, 603)
        self.gridLayout = QGridLayout(Img)
        self.gridLayout.setObjectName(u"gridLayout")
        self.graphicsView = QGraphicsView(Img)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.line_2 = QFrame(Img)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_8 = QLabel(Img)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_8.addWidget(self.label_8)

        self.resolutionLabel = QLabel(Img)
        self.resolutionLabel.setObjectName(u"resolutionLabel")

        self.horizontalLayout_8.addWidget(self.resolutionLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_10 = QLabel(Img)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_9.addWidget(self.label_10)

        self.sizeLabel = QLabel(Img)
        self.sizeLabel.setObjectName(u"sizeLabel")

        self.horizontalLayout_9.addWidget(self.sizeLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_6 = QLabel(Img)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_10.addWidget(self.label_6)

        self.tickLabel = QLabel(Img)
        self.tickLabel.setObjectName(u"tickLabel")

        self.horizontalLayout_10.addWidget(self.tickLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

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

        self.line = QFrame(Img)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkBox = QCheckBox(Img)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.scaleRadio = QRadioButton(Img)
        self.buttonGroup_2 = QButtonGroup(Img)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.scaleRadio)
        self.scaleRadio.setObjectName(u"scaleRadio")
        self.scaleRadio.setMaximumSize(QSize(80, 16777215))
        self.scaleRadio.setChecked(True)

        self.horizontalLayout_3.addWidget(self.scaleRadio)

        self.label_3 = QLabel(Img)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.scaleEdit = QLineEdit(Img)
        self.scaleEdit.setObjectName(u"scaleEdit")
        self.scaleEdit.setMaximumSize(QSize(60, 16777215))
        self.scaleEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.scaleEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.heighRadio = QRadioButton(Img)
        self.buttonGroup_2.addButton(self.heighRadio)
        self.heighRadio.setObjectName(u"heighRadio")
        self.heighRadio.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_4.addWidget(self.heighRadio)

        self.label = QLabel(Img)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.widthEdit = QLineEdit(Img)
        self.widthEdit.setObjectName(u"widthEdit")
        self.widthEdit.setEnabled(False)
        self.widthEdit.setMaximumSize(QSize(60, 16777215))
        self.widthEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.widthEdit)

        self.label_2 = QLabel(Img)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.heighEdit = QLineEdit(Img)
        self.heighEdit.setObjectName(u"heighEdit")
        self.heighEdit.setEnabled(False)
        self.heighEdit.setMaximumSize(QSize(60, 16777215))
        self.heighEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.heighEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(Img)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_5.addWidget(self.label_4)

        self.radioButton_8 = QRadioButton(Img)
        self.buttonGroup = QButtonGroup(Img)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton_8)
        self.radioButton_8.setObjectName(u"radioButton_8")

        self.horizontalLayout_5.addWidget(self.radioButton_8)

        self.radioButton_5 = QRadioButton(Img)
        self.buttonGroup.addButton(self.radioButton_5)
        self.radioButton_5.setObjectName(u"radioButton_5")

        self.horizontalLayout_5.addWidget(self.radioButton_5)

        self.radioButton_6 = QRadioButton(Img)
        self.buttonGroup.addButton(self.radioButton_6)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.horizontalLayout_5.addWidget(self.radioButton_6)

        self.radioButton_4 = QRadioButton(Img)
        self.buttonGroup.addButton(self.radioButton_4)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.horizontalLayout_5.addWidget(self.radioButton_4)

        self.radioButton_7 = QRadioButton(Img)
        self.buttonGroup.addButton(self.radioButton_7)
        self.radioButton_7.setObjectName(u"radioButton_7")
        self.radioButton_7.setChecked(True)

        self.horizontalLayout_5.addWidget(self.radioButton_7)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(Img)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_6.addWidget(self.label_5)

        self.comboBox = QComboBox(Img)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMaximumSize(QSize(130, 16777215))

        self.horizontalLayout_6.addWidget(self.comboBox)

        self.ttaModel = QCheckBox(Img)
        self.ttaModel.setObjectName(u"ttaModel")

        self.horizontalLayout_6.addWidget(self.ttaModel)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")

        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.changeButton = QPushButton(Img)
        self.changeButton.setObjectName(u"changeButton")
        self.changeButton.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_2.addWidget(self.changeButton)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.line_3 = QFrame(Img)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)


        self.retranslateUi(Img)
        self.changeButton.clicked.connect(Img.StartWaifu2x)
        self.saveButton.clicked.connect(Img.SavePicture)
        self.pushButton_3.clicked.connect(Img.ReduceScalePic)
        self.pushButton.clicked.connect(Img.AddScalePic)
        self.oepnButton.clicked.connect(Img.OpenPicture)
        self.comboBox.currentIndexChanged.connect(Img.ChangeModel)
        self.scaleRadio.clicked.connect(Img.CheckScaleRadio)
        self.heighRadio.clicked.connect(Img.CheckScaleRadio)
        self.radioButton_8.clicked.connect(Img.CheckScaleRadio)
        self.radioButton_5.clicked.connect(Img.CheckScaleRadio)
        self.radioButton_6.clicked.connect(Img.CheckScaleRadio)
        self.radioButton_4.clicked.connect(Img.CheckScaleRadio)
        self.radioButton_7.clicked.connect(Img.CheckScaleRadio)
        self.ttaModel.clicked.connect(Img.CheckScaleRadio)
        self.checkBox.clicked.connect(Img.SwithPicture)
        self.widthEdit.textChanged.connect(Img.CheckScaleRadio)
        self.heighEdit.textChanged.connect(Img.CheckScaleRadio)
        self.scaleEdit.textChanged.connect(Img.CheckScaleRadio)

        QMetaObject.connectSlotsByName(Img)
    # setupUi

    def retranslateUi(self, Img):
        Img.setWindowTitle(QCoreApplication.translate("Img", u"Form", None))
        self.label_8.setText(QCoreApplication.translate("Img", u"\u5206\u8fa8\u7387\uff1a", None))
        self.resolutionLabel.setText(QCoreApplication.translate("Img", u"TextLabel", None))
        self.label_10.setText(QCoreApplication.translate("Img", u"\u5927 \u5c0f\uff1a", None))
        self.sizeLabel.setText(QCoreApplication.translate("Img", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("Img", u"\u8017\u65f6\uff1a", None))
        self.tickLabel.setText("")
        self.oepnButton.setText(QCoreApplication.translate("Img", u"\u6253\u5f00\u56fe\u7247", None))
        self.pushButton_3.setText(QCoreApplication.translate("Img", u"\u7f29\u5c0f", None))
        self.pushButton.setText(QCoreApplication.translate("Img", u"\u653e\u5927", None))
        self.saveButton.setText(QCoreApplication.translate("Img", u"\u4fdd\u5b58\u56fe\u7247", None))
        self.checkBox.setText(QCoreApplication.translate("Img", u"waifu2x", None))
        self.scaleRadio.setText(QCoreApplication.translate("Img", u"\u500d\u6570\u653e\u5927", None))
        self.label_3.setText(QCoreApplication.translate("Img", u"\u653e\u5927\u500d\u6570", None))
        self.scaleEdit.setText(QCoreApplication.translate("Img", u"2", None))
        self.heighRadio.setText(QCoreApplication.translate("Img", u"\u56fa\u5b9a\u957f\u5bbd", None))
        self.label.setText(QCoreApplication.translate("Img", u"\u957f", None))
        self.label_2.setText(QCoreApplication.translate("Img", u"\u5bbd", None))
        self.label_4.setText(QCoreApplication.translate("Img", u"\u964d\u566a\u7b49\u7ea7\uff1a", None))
        self.radioButton_8.setText(QCoreApplication.translate("Img", u"-1", None))
        self.radioButton_5.setText(QCoreApplication.translate("Img", u"0", None))
        self.radioButton_6.setText(QCoreApplication.translate("Img", u"1", None))
        self.radioButton_4.setText(QCoreApplication.translate("Img", u"2", None))
        self.radioButton_7.setText(QCoreApplication.translate("Img", u"3", None))
        self.label_5.setText(QCoreApplication.translate("Img", u"\u6a21\u578b\uff1a", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Img", u"cunet", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Img", u"photo", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Img", u"anime_style_art_rgb", None))

#if QT_CONFIG(tooltip)
        self.ttaModel.setToolTip(QCoreApplication.translate("Img", u"\u753b\u8d28\u63d0\u5347\uff0c\u8017\u65f6\u589e\u52a0", None))
#endif // QT_CONFIG(tooltip)
        self.ttaModel.setText(QCoreApplication.translate("Img", u"tta\u6a21\u5f0f", None))
        self.changeButton.setText(QCoreApplication.translate("Img", u"\u8f6c\u6362", None))
    # retranslateUi

