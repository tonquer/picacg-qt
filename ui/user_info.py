# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user_info.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .head_label import HeadLabel


class Ui_UserInfo(object):
    def setupUi(self, UserInfo):
        if not UserInfo.objectName():
            UserInfo.setObjectName(u"UserInfo")
        UserInfo.resize(658, 213)
        self.gridLayout = QGridLayout(UserInfo)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.indexLabel = QLabel(UserInfo)
        self.indexLabel.setObjectName(u"indexLabel")
        self.indexLabel.setMinimumSize(QSize(100, 0))
        self.indexLabel.setMaximumSize(QSize(100, 30))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(10)
        self.indexLabel.setFont(font)
        self.indexLabel.setLayoutDirection(Qt.RightToLeft)
        self.indexLabel.setStyleSheet(u"color: #999999;")
        self.indexLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.indexLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.picIcon = HeadLabel(UserInfo)
        self.picIcon.setObjectName(u"picIcon")
        self.picIcon.setMinimumSize(QSize(100, 100))
        self.picIcon.setMaximumSize(QSize(100, 100))
        self.picIcon.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.picIcon, 0, Qt.AlignHCenter)

        self.dateLabel = QLabel(UserInfo)
        self.dateLabel.setObjectName(u"dateLabel")
        self.dateLabel.setMinimumSize(QSize(100, 0))
        self.dateLabel.setMaximumSize(QSize(100, 30))
        self.dateLabel.setFont(font)
        self.dateLabel.setStyleSheet(u"color: #999999;")
        self.dateLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.dateLabel)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.nameLabel = QLabel(UserInfo)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setMinimumSize(QSize(0, 20))
        self.nameLabel.setMaximumSize(QSize(16777215, 20))
        self.nameLabel.setFont(font)
        self.nameLabel.setLayoutDirection(Qt.LeftToRight)
        self.nameLabel.setStyleSheet(u"")
        self.nameLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.nameLabel)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.levelLabel = QLabel(UserInfo)
        self.levelLabel.setObjectName(u"levelLabel")
        self.levelLabel.setMinimumSize(QSize(0, 20))
        self.levelLabel.setMaximumSize(QSize(16777215, 20))
        self.levelLabel.setStyleSheet(u"color: rgb(196, 95, 125);")

        self.horizontalLayout_4.addWidget(self.levelLabel)

        self.titleLabel = QLabel(UserInfo)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setMinimumSize(QSize(0, 20))
        self.titleLabel.setMaximumSize(QSize(16777215, 20))
        self.titleLabel.setStyleSheet(u"color: rgb(196, 95, 125);")

        self.horizontalLayout_4.addWidget(self.titleLabel)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.commentLabel = QLabel(UserInfo)
        self.commentLabel.setObjectName(u"commentLabel")
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font1.setPointSize(12)
        self.commentLabel.setFont(font1)

        self.verticalLayout_3.addWidget(self.commentLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.starButton = QToolButton(UserInfo)
        self.starButton.setObjectName(u"starButton")
        self.starButton.setStyleSheet(u"background-color:transparent;")

        self.horizontalLayout_3.addWidget(self.starButton)

        self.horizontalSpacer_2 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.retranslateUi(UserInfo)
        self.starButton.clicked.connect(UserInfo.AddLike)

        QMetaObject.connectSlotsByName(UserInfo)
    # setupUi

    def retranslateUi(self, UserInfo):
        UserInfo.setWindowTitle(QCoreApplication.translate("UserInfo", u"Form", None))
        self.indexLabel.setText(QCoreApplication.translate("UserInfo", u"TextLabel", None))
        self.picIcon.setText(QCoreApplication.translate("UserInfo", u"TextLabel", None))
        self.dateLabel.setText("")
        self.nameLabel.setText(QCoreApplication.translate("UserInfo", u"TextLabel", None))
        self.levelLabel.setText(QCoreApplication.translate("UserInfo", u"LV", None))
        self.titleLabel.setText(QCoreApplication.translate("UserInfo", u"TextLabel", None))
        self.commentLabel.setText(QCoreApplication.translate("UserInfo", u"TextLabel", None))
        self.starButton.setText(QCoreApplication.translate("UserInfo", u"...", None))
    # retranslateUi

