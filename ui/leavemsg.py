# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'leavemsg.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_LeaveMsg(object):
    def setupUi(self, LeaveMsg):
        if not LeaveMsg.objectName():
            LeaveMsg.setObjectName(u"LeaveMsg")
        LeaveMsg.resize(400, 292)
        self.gridLayout_2 = QGridLayout(LeaveMsg)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.nums = QLabel(LeaveMsg)
        self.nums.setObjectName(u"nums")

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(LeaveMsg)
        self.pages.setObjectName(u"pages")

        self.horizontalLayout.addWidget(self.pages)

        self.lineEdit = QLineEdit(LeaveMsg)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.jumpButton = QPushButton(LeaveMsg)
        self.jumpButton.setObjectName(u"jumpButton")

        self.horizontalLayout.addWidget(self.jumpButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 1, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")

        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.retranslateUi(LeaveMsg)
        self.jumpButton.clicked.connect(LeaveMsg.JumpPage)

        QMetaObject.connectSlotsByName(LeaveMsg)
    # setupUi

    def retranslateUi(self, LeaveMsg):
        LeaveMsg.setWindowTitle(QCoreApplication.translate("LeaveMsg", u"Form", None))
        self.nums.setText(QCoreApplication.translate("LeaveMsg", u"\u5206\u9875\uff1a", None))
        self.pages.setText(QCoreApplication.translate("LeaveMsg", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("LeaveMsg", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("LeaveMsg", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

