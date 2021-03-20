# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chatrootmsg.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ChatRoomMsg(object):
    def setupUi(self, ChatRoomMsg):
        if not ChatRoomMsg.objectName():
            ChatRoomMsg.setObjectName(u"ChatRoomMsg")
        ChatRoomMsg.resize(400, 197)
        self.gridLayout_2 = QGridLayout(ChatRoomMsg)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.picLabel = QLabel(ChatRoomMsg)
        self.picLabel.setObjectName(u"picLabel")
        self.picLabel.setMinimumSize(QSize(80, 80))
        self.picLabel.setMaximumSize(QSize(80, 80))
        self.picLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.picLabel)

        self.nameLabel = QLabel(ChatRoomMsg)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setMinimumSize(QSize(80, 20))
        self.nameLabel.setMaximumSize(QSize(80, 20))
        self.nameLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.nameLabel)

        self.numLabel = QLabel(ChatRoomMsg)
        self.numLabel.setObjectName(u"numLabel")
        self.numLabel.setMaximumSize(QSize(80, 20))

        self.verticalLayout.addWidget(self.numLabel)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(ChatRoomMsg)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.replayLabel = QLabel(self.widget)
        self.replayLabel.setObjectName(u"replayLabel")

        self.verticalLayout_3.addWidget(self.replayLabel)

        self.commentLabel = QLabel(self.widget)
        self.commentLabel.setObjectName(u"commentLabel")

        self.verticalLayout_3.addWidget(self.commentLabel)


        self.verticalLayout_2.addWidget(self.widget)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 1, 1, 1)


        self.retranslateUi(ChatRoomMsg)

        QMetaObject.connectSlotsByName(ChatRoomMsg)
    # setupUi

    def retranslateUi(self, ChatRoomMsg):
        ChatRoomMsg.setWindowTitle(QCoreApplication.translate("ChatRoomMsg", u"Form", None))
        self.picLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.nameLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.numLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.replayLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.commentLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
    # retranslateUi

