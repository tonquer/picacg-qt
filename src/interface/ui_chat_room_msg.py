# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_chat_room_msg.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)

from component.label.head_label import HeadLabel
import images_rc

class Ui_ChatRoomMsg(object):
    def setupUi(self, ChatRoomMsg):
        if not ChatRoomMsg.objectName():
            ChatRoomMsg.setObjectName(u"ChatRoomMsg")
        ChatRoomMsg.resize(636, 248)
        ChatRoomMsg.setStyleSheet(u"QWidget#widget{\n"
"            border-image:url(:png/icon/skin_aio_friend_bubble_pressed.9.png) 50;\n"
"			border-width: 45;\n"
"			margin-top: -5;\n"
"			margin-left: -5;\n"
"			margin-right: -5;\n"
"			margin-bottom: -5;\n"
"            }\n"
"\n"
"QWidget#replayWidget\n"
"{\n"
"background: transparent;    \n"
"            border-image:url(:png/icon/skin_aio_friend_bubble_pressed.9.png) 50;\n"
"			border-width: 55;\n"
"			margin-top: -5;\n"
"			margin-left: -5;\n"
"			margin-right: -5;\n"
"			margin-bottom: -5;\n"
"\n"
"}")
        self.gridLayout_2 = QGridLayout(ChatRoomMsg)
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 1, -1, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.picLabel = HeadLabel(ChatRoomMsg)
        self.picLabel.setObjectName(u"picLabel")
        self.picLabel.setMinimumSize(QSize(100, 100))
        self.picLabel.setMaximumSize(QSize(100, 100))
        self.picLabel.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.picLabel, 0, Qt.AlignTop)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.nameLabel = QLabel(ChatRoomMsg)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setMinimumSize(QSize(0, 20))
        self.nameLabel.setMaximumSize(QSize(16777215, 30))
        font = QFont()
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
        self.widget.setMinimumSize(QSize(0, 100))
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.replayWidget = QWidget(self.widget)
        self.replayWidget.setObjectName(u"replayWidget")
        self.replayWidget.setMinimumSize(QSize(0, 100))
        self.horizontalLayout_2 = QHBoxLayout(self.replayWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.replayLabel = QLabel(self.replayWidget)
        self.replayLabel.setObjectName(u"replayLabel")
        self.replayLabel.setMinimumSize(QSize(40, 50))
        self.replayLabel.setFont(font)
        self.replayLabel.setStyleSheet(u"padding-left:20px;\n"
"padding-right:10px;")

        self.horizontalLayout_2.addWidget(self.replayLabel)


        self.verticalLayout_3.addWidget(self.replayWidget)

        self.commentLabel = QLabel(self.widget)
        self.commentLabel.setObjectName(u"commentLabel")
        self.commentLabel.setMinimumSize(QSize(0, 0))
        self.commentLabel.setFont(font)
        self.commentLabel.setStyleSheet(u"padding-left:10px;\n"
"padding-top:25px;\n"
"padding-right:10px;")

        self.verticalLayout_3.addWidget(self.commentLabel)

        self.toolButton = QToolButton(self.widget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setStyleSheet(u"padding-left:15px;\n"
"padding-right:10px;")

        self.verticalLayout_3.addWidget(self.toolButton)

        self.infoLabel = QLabel(self.widget)
        self.infoLabel.setObjectName(u"infoLabel")
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(True)
        font1.setItalic(True)
        font1.setUnderline(False)
        self.infoLabel.setFont(font1)
        self.infoLabel.setStyleSheet(u"color: #999999;\n"
"padding-left:15px;\n"
"padding-right:15px;")
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
        self.nameLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.indexLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"X\u697c", None))
        self.levelLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"LV", None))
        self.titleLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.replayLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.commentLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
        self.toolButton.setText(QCoreApplication.translate("ChatRoomMsg", u"...", None))
        self.infoLabel.setText(QCoreApplication.translate("ChatRoomMsg", u"TextLabel", None))
    # retranslateUi

