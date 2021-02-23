# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(657, 205)
        self.gridLayout = QGridLayout(Login)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.loginButton = QPushButton(Login)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setMinimumSize(QSize(100, 30))
        self.loginButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.loginButton)

        self.registerButton = QPushButton(Login)
        self.registerButton.setObjectName(u"registerButton")
        self.registerButton.setMinimumSize(QSize(100, 30))
        self.registerButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.registerButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Login)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(50, 30))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.passwdEdit = QLineEdit(Login)
        self.passwdEdit.setObjectName(u"passwdEdit")
        self.passwdEdit.setMinimumSize(QSize(300, 30))
        self.passwdEdit.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_2.addWidget(self.passwdEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Login)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(50, 30))
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.userIdEdit = QLineEdit(Login)
        self.userIdEdit.setObjectName(u"userIdEdit")
        self.userIdEdit.setMinimumSize(QSize(300, 30))

        self.horizontalLayout.addWidget(self.userIdEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(Login)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.selectIp1 = QRadioButton(Login)
        self.selectIp1.setObjectName(u"selectIp1")

        self.horizontalLayout_4.addWidget(self.selectIp1)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 2, 1, 1, 1)

        QWidget.setTabOrder(self.userIdEdit, self.passwdEdit)
        QWidget.setTabOrder(self.passwdEdit, self.loginButton)
        QWidget.setTabOrder(self.loginButton, self.registerButton)
        QWidget.setTabOrder(self.registerButton, self.selectIp1)

        self.retranslateUi(Login)
        self.loginButton.clicked.connect(Login.Login)
        self.registerButton.clicked.connect(Login.OpenRegister)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Form", None))
        self.loginButton.setText(QCoreApplication.translate("Login", u"\u767b\u9646", None))
        self.registerButton.setText(QCoreApplication.translate("Login", u"\u6ce8\u518c", None))
        self.label_2.setText(QCoreApplication.translate("Login", u"\u5bc6\u7801", None))
        self.passwdEdit.setText("")
        self.label.setText(QCoreApplication.translate("Login", u"\u5e10\u53f7", None))
        self.userIdEdit.setText("")
        self.label_3.setText(QCoreApplication.translate("Login", u"\u5982\u679c\u4e0d\u80fd\u8fde\u63a5\u548c\u770b\u56fe\uff0c\u8bf7\u5c1d\u8bd5\u5176\u4ed6\u5206\u6d41", None))
        self.selectIp1.setText(QCoreApplication.translate("Login", u"\u5206\u6d411", None))
    # retranslateUi

