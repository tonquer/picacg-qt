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

from .qtlistwidget import QtBookList


class Ui_LeaveMsg(object):
    def setupUi(self, LeaveMsg):
        if not LeaveMsg.objectName():
            LeaveMsg.setObjectName(u"LeaveMsg")
        LeaveMsg.resize(699, 399)
        self.gridLayout_2 = QGridLayout(LeaveMsg)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 1, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.commentLine = QLineEdit(LeaveMsg)
        self.commentLine.setObjectName(u"commentLine")
        self.commentLine.setMinimumSize(QSize(0, 30))
        self.commentLine.setStyleSheet(u"background-color:transparent;")

        self.horizontalLayout_2.addWidget(self.commentLine)

        self.commentButton = QPushButton(LeaveMsg)
        self.commentButton.setObjectName(u"commentButton")
        self.commentButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.commentButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.line = QFrame(LeaveMsg)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line)

        self.nums = QLabel(LeaveMsg)
        self.nums.setObjectName(u"nums")
        self.nums.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.nums)

        self.pages = QLabel(LeaveMsg)
        self.pages.setObjectName(u"pages")
        self.pages.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.pages)

        self.line_2 = QFrame(LeaveMsg)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line_2)

        self.spinBox = QSpinBox(LeaveMsg)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 30))
        self.spinBox.setStyleSheet(u"background-color:transparent;")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout_2.addWidget(self.spinBox)

        self.line_3 = QFrame(LeaveMsg)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line_3)

        self.jumpButton = QPushButton(LeaveMsg)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.jumpButton)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.listWidget = QtBookList(LeaveMsg)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
"QListWidget::item { border-bottom: 1px solid black; }")

        self.gridLayout_3.addWidget(self.listWidget, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.retranslateUi(LeaveMsg)
        self.jumpButton.clicked.connect(LeaveMsg.JumpPage)

        QMetaObject.connectSlotsByName(LeaveMsg)
    # setupUi

    def retranslateUi(self, LeaveMsg):
        LeaveMsg.setWindowTitle(QCoreApplication.translate("LeaveMsg", u"Form", None))
        self.commentButton.setText(QCoreApplication.translate("LeaveMsg", u"\u53d1\u9001\u8bc4\u8bba", None))
#if QT_CONFIG(shortcut)
        self.commentButton.setShortcut(QCoreApplication.translate("LeaveMsg", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.nums.setText(QCoreApplication.translate("LeaveMsg", u"\u5206\u9875\uff1a", None))
        self.pages.setText(QCoreApplication.translate("LeaveMsg", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("LeaveMsg", u"\u8df3\u8f6c", None))
    # retranslateUi

