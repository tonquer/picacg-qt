# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_User(object):
    def setupUi(self, User):
        if not User.objectName():
            User.setObjectName(u"User")
        User.resize(801, 488)
        User.setMinimumSize(QSize(0, 0))
        self.gridLayout_2 = QGridLayout(User)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.stackedWidget = QStackedWidget(User)
        self.stackedWidget.setObjectName(u"stackedWidget")

        self.gridLayout_2.addWidget(self.stackedWidget, 0, 1, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.icon = QLabel(User)
        self.icon.setObjectName(u"icon")
        self.icon.setEnabled(True)
        self.icon.setMinimumSize(QSize(200, 200))
        self.icon.setMaximumSize(QSize(200, 200))
        self.icon.setStyleSheet(u"background: transparent;")
        self.icon.setScaledContents(True)

        self.verticalLayout.addWidget(self.icon)

        self.exp = QLabel(User)
        self.exp.setObjectName(u"exp")
        self.exp.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout.addWidget(self.exp)

        self.level = QLabel(User)
        self.level.setObjectName(u"level")
        self.level.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout.addWidget(self.level)

        self.name = QLabel(User)
        self.name.setObjectName(u"name")
        self.name.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout.addWidget(self.name)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.sign = QLabel(User)
        self.sign.setObjectName(u"sign")
        self.sign.setMinimumSize(QSize(0, 0))
        self.sign.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.sign)

        self.signButton = QPushButton(User)
        self.signButton.setObjectName(u"signButton")
        self.signButton.setEnabled(False)
        self.signButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.signButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = QListWidget(User)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMinimumSize(QSize(0, 0))
        self.listWidget.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout.addWidget(self.listWidget)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(User)
        self.signButton.clicked.connect(User.Sign)

        QMetaObject.connectSlotsByName(User)
    # setupUi

    def retranslateUi(self, User):
        User.setWindowTitle(QCoreApplication.translate("User", u"Form", None))
        self.icon.setText("")
        self.exp.setText(QCoreApplication.translate("User", u"exp", None))
        self.level.setText(QCoreApplication.translate("User", u"level:", None))
        self.name.setText(QCoreApplication.translate("User", u"name", None))
        self.sign.setText(QCoreApplication.translate("User", u"sign:", None))
        self.signButton.setText(QCoreApplication.translate("User", u"\u5df2\u7b7e\u5230", None))
    # retranslateUi

