# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chatroom.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ChatRoom(object):
    def setupUi(self, ChatRoom):
        if not ChatRoom.objectName():
            ChatRoom.setObjectName(u"ChatRoom")
        ChatRoom.resize(530, 582)
        self.gridLayout = QGridLayout(ChatRoom)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.nameLabel = QLabel(ChatRoom)
        self.nameLabel.setObjectName(u"nameLabel")

        self.horizontalLayout_3.addWidget(self.nameLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.numLabel = QLabel(ChatRoom)
        self.numLabel.setObjectName(u"numLabel")

        self.horizontalLayout_3.addWidget(self.numLabel)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(ChatRoom)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 510, 495))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit = QLineEdit(ChatRoom)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.sendButton = QPushButton(ChatRoom)
        self.sendButton.setObjectName(u"sendButton")

        self.horizontalLayout_2.addWidget(self.sendButton)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)


        self.retranslateUi(ChatRoom)
        self.sendButton.clicked.connect(ChatRoom.SendMsg)

        QMetaObject.connectSlotsByName(ChatRoom)
    # setupUi

    def retranslateUi(self, ChatRoom):
        ChatRoom.setWindowTitle(QCoreApplication.translate("ChatRoom", u"Form", None))
        self.nameLabel.setText(QCoreApplication.translate("ChatRoom", u"TextLabel", None))
        self.numLabel.setText(QCoreApplication.translate("ChatRoom", u"TextLabel", None))
        self.sendButton.setText(QCoreApplication.translate("ChatRoom", u"\u53d1\u9001", None))
    # retranslateUi

