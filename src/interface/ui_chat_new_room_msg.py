# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_chat_new_room_msg.ui'
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

class Ui_ChatNewRoomMsg(object):
    def setupUi(self, ChatNewRoomMsg):
        if not ChatNewRoomMsg.objectName():
            ChatNewRoomMsg.setObjectName(u"ChatNewRoomMsg")
        ChatNewRoomMsg.resize(749, 299)
        ChatNewRoomMsg.setStyleSheet(u"QWidget#widget{\n"
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
        self.gridLayout_2 = QGridLayout(ChatNewRoomMsg)
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 1, -1, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.picLabel = HeadLabel(ChatNewRoomMsg)
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
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, -1, 4, -1)
        self.indexLabel = QLabel(ChatNewRoomMsg)
        self.indexLabel.setObjectName(u"indexLabel")

        self.horizontalLayout.addWidget(self.indexLabel)

        self.levelLabel = QLabel(ChatNewRoomMsg)
        self.levelLabel.setObjectName(u"levelLabel")
        self.levelLabel.setMinimumSize(QSize(0, 20))
        self.levelLabel.setMaximumSize(QSize(16777215, 20))
        self.levelLabel.setStyleSheet(u"background:#eeA2A4;")

        self.horizontalLayout.addWidget(self.levelLabel)

        self.titleLabel = QLabel(ChatNewRoomMsg)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setMinimumSize(QSize(0, 20))
        self.titleLabel.setMaximumSize(QSize(16777215, 20))
        self.titleLabel.setStyleSheet(u"background:#eeA2A4;")

        self.horizontalLayout.addWidget(self.titleLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.widget = QWidget(ChatNewRoomMsg)
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
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.replyPic = QLabel(self.replayWidget)
        self.replyPic.setObjectName(u"replyPic")
        self.replyPic.setStyleSheet(u"padding-left:20px;\n"
"padding-top:20px;")

        self.horizontalLayout_3.addWidget(self.replyPic)

        self.replayLabel = QLabel(self.replayWidget)
        self.replayLabel.setObjectName(u"replayLabel")
        self.replayLabel.setMinimumSize(QSize(40, 50))
        font = QFont()
        font.setPointSize(12)
        self.replayLabel.setFont(font)
        self.replayLabel.setStyleSheet(u"padding-left:20px;\n"
"padding-right:10px;")

        self.horizontalLayout_3.addWidget(self.replayLabel)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addWidget(self.replayWidget)

        self.commentLabel = QLabel(self.widget)
        self.commentLabel.setObjectName(u"commentLabel")
        self.commentLabel.setMinimumSize(QSize(0, 0))
        self.commentLabel.setFont(font)
        self.commentLabel.setStyleSheet(u"padding-left:10px;\n"
"padding-top:25px;\n"
"padding-right:10px;")

        self.verticalLayout_3.addWidget(self.commentLabel)

        self.pic2Label = QLabel(self.widget)
        self.pic2Label.setObjectName(u"pic2Label")
        self.pic2Label.setFont(font)
        self.pic2Label.setStyleSheet(u"padding-left:10px;\n"
"padding-top:25px;\n"
"padding-right:10px;")

        self.verticalLayout_3.addWidget(self.pic2Label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

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


        self.gridLayout.addWidget(self.widget, 5, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.nameLabel = QLabel(ChatNewRoomMsg)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setMinimumSize(QSize(0, 20))
        self.nameLabel.setMaximumSize(QSize(16777215, 30))
        self.nameLabel.setFont(font)

        self.horizontalLayout_4.addWidget(self.nameLabel)

        self.vipIcon = QToolButton(ChatNewRoomMsg)
        self.vipIcon.setObjectName(u"vipIcon")
        icon = QIcon()
        icon.addFile(u":/png/icon/vip.png", QSize(), QIcon.Normal, QIcon.Off)
        self.vipIcon.setIcon(icon)
        self.vipIcon.setIconSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.vipIcon)

        self.managerIcon = QToolButton(ChatNewRoomMsg)
        self.managerIcon.setObjectName(u"managerIcon")
        icon1 = QIcon()
        icon1.addFile(u":/png/icon/svip.png", QSize(), QIcon.Normal, QIcon.Off)
        self.managerIcon.setIcon(icon1)
        self.managerIcon.setIconSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.managerIcon)

        self.nvIcon = QToolButton(ChatNewRoomMsg)
        self.nvIcon.setObjectName(u"nvIcon")
        icon2 = QIcon()
        icon2.addFile(u":/png/icon/nv.png", QSize(), QIcon.Normal, QIcon.Off)
        self.nvIcon.setIcon(icon2)
        self.nvIcon.setIconSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.nvIcon)

        self.officialIcon = QToolButton(ChatNewRoomMsg)
        self.officialIcon.setObjectName(u"officialIcon")
        icon3 = QIcon()
        icon3.addFile(u":/png/icon/icon_picacg.png", QSize(), QIcon.Normal, QIcon.Off)
        self.officialIcon.setIcon(icon3)
        self.officialIcon.setIconSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.officialIcon)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)


        self.retranslateUi(ChatNewRoomMsg)

        QMetaObject.connectSlotsByName(ChatNewRoomMsg)
    # setupUi

    def retranslateUi(self, ChatNewRoomMsg):
        ChatNewRoomMsg.setWindowTitle(QCoreApplication.translate("ChatNewRoomMsg", u"Form", None))
        self.picLabel.setText("")
        self.indexLabel.setText(QCoreApplication.translate("ChatNewRoomMsg", u"X\u697c", None))
        self.levelLabel.setText(QCoreApplication.translate("ChatNewRoomMsg", u"LV", None))
        self.titleLabel.setText(QCoreApplication.translate("ChatNewRoomMsg", u"TextLabel", None))
        self.replyPic.setText("")
        self.replayLabel.setText(QCoreApplication.translate("ChatNewRoomMsg", u"TextLabel", None))
        self.commentLabel.setText(QCoreApplication.translate("ChatNewRoomMsg", u"TextLabel", None))
        self.pic2Label.setText("")
        self.infoLabel.setText(QCoreApplication.translate("ChatNewRoomMsg", u"TextLabel", None))
        self.nameLabel.setText(QCoreApplication.translate("ChatNewRoomMsg", u"TextLabel", None))
#if QT_CONFIG(tooltip)
        self.vipIcon.setToolTip(QCoreApplication.translate("ChatNewRoomMsg", u"vip\u7528\u6237", None))
#endif // QT_CONFIG(tooltip)
        self.vipIcon.setText(QCoreApplication.translate("ChatNewRoomMsg", u"...", None))
#if QT_CONFIG(tooltip)
        self.managerIcon.setToolTip(QCoreApplication.translate("ChatNewRoomMsg", u"\u623f\u7ba1", None))
#endif // QT_CONFIG(tooltip)
        self.managerIcon.setText("")
#if QT_CONFIG(tooltip)
        self.nvIcon.setToolTip(QCoreApplication.translate("ChatNewRoomMsg", u"\u5973\u83e9\u8428", None))
#endif // QT_CONFIG(tooltip)
        self.nvIcon.setText(QCoreApplication.translate("ChatNewRoomMsg", u"...", None))
#if QT_CONFIG(tooltip)
        self.officialIcon.setToolTip(QCoreApplication.translate("ChatNewRoomMsg", u"\u54d4\u5494\u5b98\u65b9", None))
#endif // QT_CONFIG(tooltip)
        self.officialIcon.setText(QCoreApplication.translate("ChatNewRoomMsg", u"...", None))
    # retranslateUi

