# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fried.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Ui_Fried(object):
    def setupUi(self, Ui_Fried):
        if not Ui_Fried.objectName():
            Ui_Fried.setObjectName(u"Ui_Fried")
        Ui_Fried.resize(721, 325)
        self.verticalLayout_3 = QVBoxLayout(Ui_Fried)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(Ui_Fried)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 707, 273))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.line_2 = QFrame(Ui_Fried)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.label = QLabel(Ui_Fried)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.label)

        self.pageLabel = QLabel(Ui_Fried)
        self.pageLabel.setObjectName(u"pageLabel")
        self.pageLabel.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.pageLabel)

        self.line = QFrame(Ui_Fried)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.spinBox = QSpinBox(Ui_Fried)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 30))
        self.spinBox.setStyleSheet(u"background-color:transparent;")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_3 = QFrame(Ui_Fried)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.pushButton = QPushButton(Ui_Fried)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.retranslateUi(Ui_Fried)
        self.pushButton.clicked.connect(Ui_Fried.JumpPage)

        QMetaObject.connectSlotsByName(Ui_Fried)
    # setupUi

    def retranslateUi(self, Ui_Fried):
        Ui_Fried.setWindowTitle(QCoreApplication.translate("Ui_Fried", u"Form", None))
        self.label.setText(QCoreApplication.translate("Ui_Fried", u"\u5206\u9875\uff1a", None))
        self.pageLabel.setText(QCoreApplication.translate("Ui_Fried", u"1/1", None))
        self.pushButton.setText(QCoreApplication.translate("Ui_Fried", u"\u8df3\u8f6c", None))
    # retranslateUi

