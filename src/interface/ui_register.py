# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_register.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtWidgets import (QButtonGroup, QDateEdit, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QRadioButton,
                               QWidget)

class Ui_Register(object):
    def setupUi(self, Register):
        if not Register.objectName():
            Register.setObjectName(u"Register")
        Register.resize(388, 412)
        self.gridLayout_2 = QGridLayout(Register)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.question3 = QLabel(Register)
        self.question3.setObjectName(u"question3")
        self.question3.setMinimumSize(QSize(80, 0))
        self.question3.setMaximumSize(QSize(60, 16777215))
        self.question3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.question3)

        self.question3Edit = QLineEdit(Register)
        self.question3Edit.setObjectName(u"question3Edit")

        self.horizontalLayout_12.addWidget(self.question3Edit)


        self.gridLayout.addLayout(self.horizontalLayout_12, 18, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.name = QLabel(Register)
        self.name.setObjectName(u"name")
        self.name.setMinimumSize(QSize(80, 0))
        self.name.setMaximumSize(QSize(60, 16777215))
        self.name.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.name)

        self.nameEdit = QLineEdit(Register)
        self.nameEdit.setObjectName(u"nameEdit")

        self.horizontalLayout.addWidget(self.nameEdit)


        self.gridLayout.addLayout(self.horizontalLayout, 11, 1, 1, 1)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.question1 = QLabel(Register)
        self.question1.setObjectName(u"question1")
        self.question1.setMinimumSize(QSize(80, 0))
        self.question1.setMaximumSize(QSize(60, 16777215))
        self.question1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_17.addWidget(self.question1)

        self.question1Edit = QLineEdit(Register)
        self.question1Edit.setObjectName(u"question1Edit")

        self.horizontalLayout_17.addWidget(self.question1Edit)


        self.gridLayout.addLayout(self.horizontalLayout_17, 14, 1, 1, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.question2 = QLabel(Register)
        self.question2.setObjectName(u"question2")
        self.question2.setMinimumSize(QSize(80, 0))
        self.question2.setMaximumSize(QSize(60, 16777215))
        self.question2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_14.addWidget(self.question2)

        self.question2Edit = QLineEdit(Register)
        self.question2Edit.setObjectName(u"question2Edit")

        self.horizontalLayout_14.addWidget(self.question2Edit)


        self.gridLayout.addLayout(self.horizontalLayout_14, 16, 1, 1, 1)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.passwd = QLabel(Register)
        self.passwd.setObjectName(u"passwd")
        self.passwd.setMinimumSize(QSize(80, 0))
        self.passwd.setMaximumSize(QSize(60, 16777215))
        self.passwd.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_19.addWidget(self.passwd)

        self.passwdEdit = QLineEdit(Register)
        self.passwdEdit.setObjectName(u"passwdEdit")

        self.horizontalLayout_19.addWidget(self.passwdEdit)


        self.gridLayout.addLayout(self.horizontalLayout_19, 12, 1, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.answer3 = QLabel(Register)
        self.answer3.setObjectName(u"answer3")
        self.answer3.setMinimumSize(QSize(80, 0))
        self.answer3.setMaximumSize(QSize(60, 16777215))
        self.answer3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.answer3)

        self.answer3Edit = QLineEdit(Register)
        self.answer3Edit.setObjectName(u"answer3Edit")

        self.horizontalLayout_11.addWidget(self.answer3Edit)


        self.gridLayout.addLayout(self.horizontalLayout_11, 19, 1, 1, 1)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.answer2 = QLabel(Register)
        self.answer2.setObjectName(u"answer2")
        self.answer2.setMinimumSize(QSize(80, 0))
        self.answer2.setMaximumSize(QSize(60, 16777215))
        self.answer2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.answer2)

        self.answer2Edit = QLineEdit(Register)
        self.answer2Edit.setObjectName(u"answer2Edit")

        self.horizontalLayout_13.addWidget(self.answer2Edit)


        self.gridLayout.addLayout(self.horizontalLayout_13, 17, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.user = QLabel(Register)
        self.user.setObjectName(u"user")
        self.user.setMinimumSize(QSize(80, 0))
        self.user.setMaximumSize(QSize(60, 16777215))
        self.user.setLayoutDirection(Qt.LeftToRight)
        self.user.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.user)

        self.userEdit = QLineEdit(Register)
        self.userEdit.setObjectName(u"userEdit")
        self.userEdit.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_3.addWidget(self.userEdit)


        self.gridLayout.addLayout(self.horizontalLayout_3, 10, 1, 1, 1)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.answer1 = QLabel(Register)
        self.answer1.setObjectName(u"answer1")
        self.answer1.setMinimumSize(QSize(80, 0))
        self.answer1.setMaximumSize(QSize(60, 16777215))
        self.answer1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.answer1)

        self.answer1Edit = QLineEdit(Register)
        self.answer1Edit.setObjectName(u"answer1Edit")

        self.horizontalLayout_15.addWidget(self.answer1Edit)


        self.gridLayout.addLayout(self.horizontalLayout_15, 15, 1, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.gender_m = QRadioButton(Register)
        self.buttonGroup = QButtonGroup(Register)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.gender_m)
        self.gender_m.setObjectName(u"gender_m")

        self.horizontalLayout_10.addWidget(self.gender_m)

        self.gender_f = QRadioButton(Register)
        self.buttonGroup.addButton(self.gender_f)
        self.gender_f.setObjectName(u"gender_f")

        self.horizontalLayout_10.addWidget(self.gender_f)

        self.gender_bot = QRadioButton(Register)
        self.buttonGroup.addButton(self.gender_bot)
        self.gender_bot.setObjectName(u"gender_bot")

        self.horizontalLayout_10.addWidget(self.gender_bot)


        self.gridLayout.addLayout(self.horizontalLayout_10, 20, 1, 1, 1)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.birthday = QLabel(Register)
        self.birthday.setObjectName(u"birthday")
        self.birthday.setMinimumSize(QSize(80, 0))
        self.birthday.setMaximumSize(QSize(60, 16777215))
        self.birthday.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_18.addWidget(self.birthday)

        self.birthdayEdit = QDateEdit(Register)
        self.birthdayEdit.setObjectName(u"birthdayEdit")

        self.horizontalLayout_18.addWidget(self.birthdayEdit)


        self.gridLayout.addLayout(self.horizontalLayout_18, 13, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.userEdit, self.nameEdit)
        QWidget.setTabOrder(self.nameEdit, self.passwdEdit)
        QWidget.setTabOrder(self.passwdEdit, self.birthdayEdit)
        QWidget.setTabOrder(self.birthdayEdit, self.question1Edit)
        QWidget.setTabOrder(self.question1Edit, self.answer1Edit)
        QWidget.setTabOrder(self.answer1Edit, self.question2Edit)
        QWidget.setTabOrder(self.question2Edit, self.answer2Edit)
        QWidget.setTabOrder(self.answer2Edit, self.question3Edit)
        QWidget.setTabOrder(self.question3Edit, self.answer3Edit)
        QWidget.setTabOrder(self.answer3Edit, self.gender_m)
        QWidget.setTabOrder(self.gender_m, self.gender_f)
        QWidget.setTabOrder(self.gender_f, self.gender_bot)

        self.retranslateUi(Register)

        QMetaObject.connectSlotsByName(Register)
    # setupUi

    def retranslateUi(self, Register):
        Register.setWindowTitle(QCoreApplication.translate("Register", u"\u65b0\u7528\u6237\u6ce8\u518c", None))
        self.question3.setText(QCoreApplication.translate("Register", u"\u95ee\u98983\uff1a", None))
        self.name.setText(QCoreApplication.translate("Register", u"\u7528\u6237\u540d\uff1a", None))
        self.question1.setText(QCoreApplication.translate("Register", u"\u95ee\u98981\uff1a", None))
        self.question2.setText(QCoreApplication.translate("Register", u"\u95ee\u98982\uff1a", None))
        self.passwd.setText(QCoreApplication.translate("Register", u"\u5bc6\u7801\uff1a", None))
        self.answer3.setText(QCoreApplication.translate("Register", u"\u7b54\u68483\uff1a", None))
        self.answer2.setText(QCoreApplication.translate("Register", u"\u7b54\u68482\uff1a", None))
        self.user.setText(QCoreApplication.translate("Register", u"\u5e10\u53f7\uff1a", None))
        self.answer1.setText(QCoreApplication.translate("Register", u"\u7b54\u68481\uff1a", None))
        self.gender_m.setText(QCoreApplication.translate("Register", u"\u7537", None))
        self.gender_f.setText(QCoreApplication.translate("Register", u"\u5973", None))
        self.gender_bot.setText(QCoreApplication.translate("Register", u"\u53cc\u6027", None))
        self.birthday.setText(QCoreApplication.translate("Register", u"\u751f\u65e5\uff1a", None))
    # retranslateUi

