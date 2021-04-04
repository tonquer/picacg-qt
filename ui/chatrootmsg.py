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
        ChatRoomMsg.resize(466, 175)
        self.gridLayout_2 = QGridLayout(ChatRoomMsg)
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 1, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(ChatRoomMsg)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(100, 100))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.picLabel = QLabel(self.frame)
        self.picLabel.setObjectName(u"picLabel")
        self.picLabel.setGeometry(QRect(10, 10, 80, 80))
        self.picLabel.setMinimumSize(QSize(80, 80))
        self.picLabel.setMaximumSize(QSize(80, 80))
        self.picLabel.setAlignment(Qt.AlignCenter)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 100, 120))
        self.label.setMinimumSize(QSize(100, 100))

        self.verticalLayout.addWidget(self.frame)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.nameLabel = QLabel(ChatRoomMsg)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setMinimumSize(QSize(0, 20))
        self.nameLabel.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(12)
        self.nameLabel.setFont(font)

        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, -1, 4, -1)
        self.indexLabel = QLabel(ChatRoomMsg)
        self.indexLabel.setObjectName(u"indexLabel")

        self.horizontalLayout.addWidget(self.indexLabel)

        self.levelLabel = QLabel(ChatRoomMsg)
        self.levelLabel.setObjectName(u"levelLabel")
        self.levelLabel.setMinimumSize(QSize(0, 20))
        self.levelLabel.setMaximumSize(QSize(16777215, 20))
        self.levelLabel.setStyleSheet(u"background:#eeA2A4;")

        self.horizontalLayout.addWidget(self.levelLabel)

        self.titleLabel = QLabel(ChatRoomMsg)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setMinimumSize(QSize(0, 20))
        self.titleLabel.setMaximumSize(QSize(16777215, 20))
        self.titleLabel.setStyleSheet(u"background:#eeA2A4;")

        self.horizontalLayout.addWidget(self.titleLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.widget = QWidget(ChatRoomMsg)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.replayLabel = QLabel(self.widget)
        self.replayLabel.setObjectName(u"replayLabel")
        self.replayLabel.setFont(font)

        self.verticalLayout_3.addWidget(self.replayLabel)

        self.commentLabel = QLabel(self.widget)
        self.commentLabel.setObjectName(u"commentLabel")
        self.commentLabel.setFont(font)

        self.verticalLayout_3.addWidget(self.commentLabel)

        self.toolButton = QToolButton(self.widget)
        self.toolButton.setObjectName(u"toolButton")

        self.verticalLayout_3.addWidget(self.toolButton)

        self.infoLabel = QLabel(self.widget)
        self.infoLabel.setObjectName(u"infoLabel")
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font1.setPointSize(8)
        font1.setBold(True)
        font1.setItalic(True)
        font1.setUnderline(False)
        font1.setWeight(75)
        self.infoLabel.setFont(font1)
        self.infoLabel.setStyleSheet(u"color: #999999;")
        self.infoLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.infoLabel)


        self.gridLayout.addWidget(self.widget, 4, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)


        self.retranslateUi(ChatRoomMsg)
        self.toolButton.clicked.connect(ChatRoomMsg.OpenAudioPath)

        QMetaObject.connectSlotsByName(ChatRoomMsg)
    # setupUi

    def retranslateUi(self, ChatRoomMsg):
        ChatRoomMsg.setWindowTitle(QCoreApplication.translate("ChatRoomMsg", u"Form", None))
        self.picLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.nameLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.indexLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"X\u697c", None))
        self.levelLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"LV", None))
        self.titleLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.replayLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.commentLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.toolButton.setText(QCoreApplication.translate("ChatRoomMsg", u"...", None))
        self.infoLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
    # retranslateUi

