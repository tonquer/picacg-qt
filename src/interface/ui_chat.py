# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_chat.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from component.list.user_list_widget import UserListWidget


class Ui_Chat(object):
    def setupUi(self, Chat):
        if not Chat.objectName():
            Chat.setObjectName(u"Chat")
        Chat.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Chat)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listWidget = UserListWidget(Chat)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)


        self.retranslateUi(Chat)

        QMetaObject.connectSlotsByName(Chat)
    # setupUi

    def retranslateUi(self, Chat):
        Chat.setWindowTitle(QCoreApplication.translate("Chat", u"\u804a\u5929\u5ba4", None))
    # retranslateUi

