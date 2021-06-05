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

from .head_label import HeadLabel


class Ui_User(object):
    def setupUi(self, User):
        if not User.objectName():
            User.setObjectName(u"User")
        User.resize(801, 637)
        User.setMinimumSize(QSize(0, 0))
        self.gridLayout_2 = QGridLayout(User)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.icon = HeadLabel(User)
        self.icon.setObjectName(u"icon")
        self.icon.setEnabled(True)
        self.icon.setMinimumSize(QSize(100, 100))
        self.icon.setMaximumSize(QSize(100, 100))
        self.icon.setStyleSheet(u"background: transparent;")
        self.icon.setScaledContents(True)

        self.verticalLayout.addWidget(self.icon)

        self.name = QLabel(User)
        self.name.setObjectName(u"name")
        self.name.setMaximumSize(QSize(100, 16777215))
        self.name.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.name)

        self.level = QLabel(User)
        self.level.setObjectName(u"level")
        self.level.setMaximumSize(QSize(100, 16777215))
        self.level.setStyleSheet(u"background:#eeA2A4;")
        self.level.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.level)

        self.title = QLabel(User)
        self.title.setObjectName(u"title")
        self.title.setMaximumSize(QSize(100, 16777215))
        self.title.setStyleSheet(u"background:#eeA2A4;")
        self.title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title)

        self.exp = QLabel(User)
        self.exp.setObjectName(u"exp")
        self.exp.setMaximumSize(QSize(100, 16777215))
        self.exp.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.exp)

        self.signButton = QPushButton(User)
        self.signButton.setObjectName(u"signButton")
        self.signButton.setEnabled(False)
        self.signButton.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout.addWidget(self.signButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.toolButton0 = QToolButton(User)
        self.buttonGroup = QButtonGroup(User)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.toolButton0)
        self.toolButton0.setObjectName(u"toolButton0")
        self.toolButton0.setMinimumSize(QSize(100, 40))
        self.toolButton0.setMaximumSize(QSize(100, 16777215))
        self.toolButton0.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton0.setCheckable(True)
        self.toolButton0.setChecked(True)

        self.verticalLayout_2.addWidget(self.toolButton0)

        self.toolButton1 = QToolButton(User)
        self.buttonGroup.addButton(self.toolButton1)
        self.toolButton1.setObjectName(u"toolButton1")
        self.toolButton1.setMinimumSize(QSize(100, 40))
        self.toolButton1.setMaximumSize(QSize(100, 16777215))
        self.toolButton1.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton1.setCheckable(True)

        self.verticalLayout_2.addWidget(self.toolButton1)

        self.toolButton2 = QToolButton(User)
        self.buttonGroup.addButton(self.toolButton2)
        self.toolButton2.setObjectName(u"toolButton2")
        self.toolButton2.setMinimumSize(QSize(100, 40))
        self.toolButton2.setMaximumSize(QSize(100, 16777215))
        self.toolButton2.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton2.setCheckable(True)

        self.verticalLayout_2.addWidget(self.toolButton2)

        self.toolButton3 = QToolButton(User)
        self.buttonGroup.addButton(self.toolButton3)
        self.toolButton3.setObjectName(u"toolButton3")
        self.toolButton3.setMinimumSize(QSize(100, 40))
        self.toolButton3.setMaximumSize(QSize(100, 16777215))
        self.toolButton3.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton3.setCheckable(True)

        self.verticalLayout_2.addWidget(self.toolButton3)

        self.toolButton4 = QToolButton(User)
        self.buttonGroup.addButton(self.toolButton4)
        self.toolButton4.setObjectName(u"toolButton4")
        self.toolButton4.setMinimumSize(QSize(100, 40))
        self.toolButton4.setMaximumSize(QSize(100, 16777215))
        self.toolButton4.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton4.setCheckable(True)

        self.verticalLayout_2.addWidget(self.toolButton4)

        self.toolButton5 = QToolButton(User)
        self.buttonGroup.addButton(self.toolButton5)
        self.toolButton5.setObjectName(u"toolButton5")
        self.toolButton5.setMinimumSize(QSize(100, 40))
        self.toolButton5.setMaximumSize(QSize(100, 16777215))
        self.toolButton5.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton5.setCheckable(True)

        self.verticalLayout_2.addWidget(self.toolButton5)

        self.toolButton6 = QToolButton(User)
        self.buttonGroup.addButton(self.toolButton6)
        self.toolButton6.setObjectName(u"toolButton6")
        self.toolButton6.setMinimumSize(QSize(100, 40))
        self.toolButton6.setMaximumSize(QSize(100, 16777215))
        self.toolButton6.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton6.setCheckable(True)

        self.verticalLayout_2.addWidget(self.toolButton6)

        self.toolButton7 = QToolButton(User)
        self.buttonGroup.addButton(self.toolButton7)
        self.toolButton7.setObjectName(u"toolButton7")
        self.toolButton7.setMinimumSize(QSize(100, 40))
        self.toolButton7.setMaximumSize(QSize(100, 16777215))
        self.toolButton7.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton7.setCheckable(True)

        self.verticalLayout_2.addWidget(self.toolButton7)

        self.toolButton8 = QToolButton(User)
        self.buttonGroup.addButton(self.toolButton8)
        self.toolButton8.setObjectName(u"toolButton8")
        self.toolButton8.setMinimumSize(QSize(100, 40))
        self.toolButton8.setMaximumSize(QSize(100, 16777215))
        self.toolButton8.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton8.setCheckable(True)

        self.verticalLayout_2.addWidget(self.toolButton8)

        self.toolButton9 = QToolButton(User)
        self.buttonGroup.addButton(self.toolButton9)
        self.toolButton9.setObjectName(u"toolButton9")
        self.toolButton9.setMinimumSize(QSize(100, 40))
        self.toolButton9.setMaximumSize(QSize(100, 16777215))
        self.toolButton9.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton9.setCheckable(True)

        self.verticalLayout_2.addWidget(self.toolButton9)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.stackedWidget = QStackedWidget(User)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"#stackedWidget {border:1px solid #014F84;}")

        self.gridLayout_2.addWidget(self.stackedWidget, 0, 1, 1, 1)


        self.retranslateUi(User)
        self.signButton.clicked.connect(User.Sign)

        QMetaObject.connectSlotsByName(User)
    # setupUi

    def retranslateUi(self, User):
        User.setWindowTitle(QCoreApplication.translate("User", u"Form", None))
        self.icon.setText("")
        self.name.setText(QCoreApplication.translate("User", u"name", None))
        self.level.setText(QCoreApplication.translate("User", u"level:", None))
        self.title.setText(QCoreApplication.translate("User", u"title", None))
        self.exp.setText(QCoreApplication.translate("User", u"exp", None))
        self.signButton.setText(QCoreApplication.translate("User", u"\u5df2\u7b7e\u5230", None))
        self.toolButton0.setText(QCoreApplication.translate("User", u"\u4e3b\u9875", None))
        self.toolButton1.setText(QCoreApplication.translate("User", u"\u641c\u7d22", None))
        self.toolButton2.setText(QCoreApplication.translate("User", u"\u5206\u7c7b", None))
        self.toolButton3.setText(QCoreApplication.translate("User", u"\u6392\u884c", None))
        self.toolButton4.setText(QCoreApplication.translate("User", u"\u6536\u85cf", None))
        self.toolButton5.setText(QCoreApplication.translate("User", u"\u5386\u53f2\u8bb0\u5f55", None))
        self.toolButton6.setText(QCoreApplication.translate("User", u"\u4e0b\u8f7d", None))
        self.toolButton7.setText(QCoreApplication.translate("User", u"\u7559\u8a00\u677f", None))
        self.toolButton8.setText(QCoreApplication.translate("User", u"\u804a\u5929\u5ba4", None))
        self.toolButton9.setText(QCoreApplication.translate("User", u"\u9505\u8d34", None))
    # retranslateUi

