# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_login_new.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QCommandLinkButton,
    QDateEdit, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTableWidgetItem, QToolButton, QVBoxLayout, QWidget)

from component.box.wheel_combo_box import WheelComboBox
from component.line_edit.tip_line_edit import TipLineEdit
from component.scroll_area.smooth_scroll_area import SmoothScrollArea
from component.tab.base_table_widget import BaseTableWidget
import images_rc

class Ui_LoginNew(object):
    def setupUi(self, LoginNew):
        if not LoginNew.objectName():
            LoginNew.setObjectName(u"LoginNew")
        LoginNew.resize(812, 690)
        self.horizontalLayout_3 = QHBoxLayout(LoginNew)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tabWidget = QTabWidget(LoginNew)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_3 = QVBoxLayout(self.tab)
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 9, 9, 9)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.widget = QWidget(self.tab)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.userEdit_2 = QLineEdit(self.widget)
        self.userEdit_2.setObjectName(u"userEdit_2")

        self.verticalLayout.addWidget(self.userEdit_2)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout.addWidget(self.label_6)

        self.passwdEdit_2 = QLineEdit(self.widget)
        self.passwdEdit_2.setObjectName(u"passwdEdit_2")
        self.passwdEdit_2.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.passwdEdit_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.saveBox = QCheckBox(self.widget)
        self.saveBox.setObjectName(u"saveBox")

        self.horizontalLayout_2.addWidget(self.saveBox)

        self.autoBox = QCheckBox(self.widget)
        self.autoBox.setObjectName(u"autoBox")

        self.horizontalLayout_2.addWidget(self.autoBox)

        self.autoSign = QCheckBox(self.widget)
        self.autoSign.setObjectName(u"autoSign")

        self.horizontalLayout_2.addWidget(self.autoSign)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.loginButton = QPushButton(self.widget)
        self.loginButton.setObjectName(u"loginButton")

        self.verticalLayout.addWidget(self.loginButton)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addWidget(self.widget)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_4 = QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.scrollArea_4 = SmoothScrollArea(self.tab_2)
        self.scrollArea_4.setObjectName(u"scrollArea_4")
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 290, 622))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.answer1 = QLabel(self.scrollAreaWidgetContents_4)
        self.answer1.setObjectName(u"answer1")
        self.answer1.setMinimumSize(QSize(80, 0))
        self.answer1.setMaximumSize(QSize(60, 16777215))
        self.answer1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_35.addWidget(self.answer1)

        self.answer1Edit = QLineEdit(self.scrollAreaWidgetContents_4)
        self.answer1Edit.setObjectName(u"answer1Edit")

        self.horizontalLayout_35.addWidget(self.answer1Edit)


        self.gridLayout_3.addLayout(self.horizontalLayout_35, 15, 1, 1, 1)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.answer3 = QLabel(self.scrollAreaWidgetContents_4)
        self.answer3.setObjectName(u"answer3")
        self.answer3.setMinimumSize(QSize(80, 0))
        self.answer3.setMaximumSize(QSize(60, 16777215))
        self.answer3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_33.addWidget(self.answer3)

        self.answer3Edit = QLineEdit(self.scrollAreaWidgetContents_4)
        self.answer3Edit.setObjectName(u"answer3Edit")

        self.horizontalLayout_33.addWidget(self.answer3Edit)


        self.gridLayout_3.addLayout(self.horizontalLayout_33, 19, 1, 1, 1)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.passwd = QLabel(self.scrollAreaWidgetContents_4)
        self.passwd.setObjectName(u"passwd")
        self.passwd.setMinimumSize(QSize(80, 0))
        self.passwd.setMaximumSize(QSize(60, 16777215))
        self.passwd.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_32.addWidget(self.passwd)

        self.passwdEdit = QLineEdit(self.scrollAreaWidgetContents_4)
        self.passwdEdit.setObjectName(u"passwdEdit")

        self.horizontalLayout_32.addWidget(self.passwdEdit)


        self.gridLayout_3.addLayout(self.horizontalLayout_32, 12, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.name = QLabel(self.scrollAreaWidgetContents_4)
        self.name.setObjectName(u"name")
        self.name.setMinimumSize(QSize(80, 0))
        self.name.setMaximumSize(QSize(60, 16777215))
        self.name.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.name)

        self.nameEdit = QLineEdit(self.scrollAreaWidgetContents_4)
        self.nameEdit.setObjectName(u"nameEdit")

        self.horizontalLayout_5.addWidget(self.nameEdit)


        self.gridLayout_3.addLayout(self.horizontalLayout_5, 11, 1, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.user = QLabel(self.scrollAreaWidgetContents_4)
        self.user.setObjectName(u"user")
        self.user.setMinimumSize(QSize(80, 0))
        self.user.setMaximumSize(QSize(60, 16777215))
        self.user.setLayoutDirection(Qt.LeftToRight)
        self.user.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.user)

        self.userEdit = QLineEdit(self.scrollAreaWidgetContents_4)
        self.userEdit.setObjectName(u"userEdit")
        self.userEdit.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_6.addWidget(self.userEdit)


        self.gridLayout_3.addLayout(self.horizontalLayout_6, 10, 1, 1, 1)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.question3 = QLabel(self.scrollAreaWidgetContents_4)
        self.question3.setObjectName(u"question3")
        self.question3.setMinimumSize(QSize(80, 0))
        self.question3.setMaximumSize(QSize(60, 16777215))
        self.question3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_19.addWidget(self.question3)

        self.question3Edit = QLineEdit(self.scrollAreaWidgetContents_4)
        self.question3Edit.setObjectName(u"question3Edit")

        self.horizontalLayout_19.addWidget(self.question3Edit)


        self.gridLayout_3.addLayout(self.horizontalLayout_19, 18, 1, 1, 1)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.birthday = QLabel(self.scrollAreaWidgetContents_4)
        self.birthday.setObjectName(u"birthday")
        self.birthday.setMinimumSize(QSize(80, 0))
        self.birthday.setMaximumSize(QSize(60, 16777215))
        self.birthday.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_36.addWidget(self.birthday)

        self.birthdayEdit = QDateEdit(self.scrollAreaWidgetContents_4)
        self.birthdayEdit.setObjectName(u"birthdayEdit")

        self.horizontalLayout_36.addWidget(self.birthdayEdit)


        self.gridLayout_3.addLayout(self.horizontalLayout_36, 13, 1, 1, 1)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.answer2 = QLabel(self.scrollAreaWidgetContents_4)
        self.answer2.setObjectName(u"answer2")
        self.answer2.setMinimumSize(QSize(80, 0))
        self.answer2.setMaximumSize(QSize(60, 16777215))
        self.answer2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_34.addWidget(self.answer2)

        self.answer2Edit = QLineEdit(self.scrollAreaWidgetContents_4)
        self.answer2Edit.setObjectName(u"answer2Edit")

        self.horizontalLayout_34.addWidget(self.answer2Edit)


        self.gridLayout_3.addLayout(self.horizontalLayout_34, 17, 1, 1, 1)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.question1 = QLabel(self.scrollAreaWidgetContents_4)
        self.question1.setObjectName(u"question1")
        self.question1.setMinimumSize(QSize(80, 0))
        self.question1.setMaximumSize(QSize(60, 16777215))
        self.question1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_30.addWidget(self.question1)

        self.question1Edit = QLineEdit(self.scrollAreaWidgetContents_4)
        self.question1Edit.setObjectName(u"question1Edit")

        self.horizontalLayout_30.addWidget(self.question1Edit)


        self.gridLayout_3.addLayout(self.horizontalLayout_30, 14, 1, 1, 1)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.question2 = QLabel(self.scrollAreaWidgetContents_4)
        self.question2.setObjectName(u"question2")
        self.question2.setMinimumSize(QSize(80, 0))
        self.question2.setMaximumSize(QSize(60, 16777215))
        self.question2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_31.addWidget(self.question2)

        self.question2Edit = QLineEdit(self.scrollAreaWidgetContents_4)
        self.question2Edit.setObjectName(u"question2Edit")

        self.horizontalLayout_31.addWidget(self.question2Edit)


        self.gridLayout_3.addLayout(self.horizontalLayout_31, 16, 1, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.gender_m = QRadioButton(self.scrollAreaWidgetContents_4)
        self.sexGroup = QButtonGroup(LoginNew)
        self.sexGroup.setObjectName(u"sexGroup")
        self.sexGroup.addButton(self.gender_m)
        self.gender_m.setObjectName(u"gender_m")

        self.horizontalLayout_10.addWidget(self.gender_m)

        self.gender_f = QRadioButton(self.scrollAreaWidgetContents_4)
        self.sexGroup.addButton(self.gender_f)
        self.gender_f.setObjectName(u"gender_f")

        self.horizontalLayout_10.addWidget(self.gender_f)

        self.gender_bot = QRadioButton(self.scrollAreaWidgetContents_4)
        self.sexGroup.addButton(self.gender_bot)
        self.gender_bot.setObjectName(u"gender_bot")
        self.gender_bot.setChecked(True)

        self.horizontalLayout_10.addWidget(self.gender_bot)


        self.gridLayout_3.addLayout(self.horizontalLayout_10, 20, 1, 1, 1)

        self.registerButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.registerButton.setObjectName(u"registerButton")

        self.gridLayout_3.addWidget(self.registerButton, 21, 1, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout_3)

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)

        self.horizontalLayout_4.addWidget(self.scrollArea_4)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.horizontalLayout_8 = QHBoxLayout(self.tab_3)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_3 = QLabel(self.tab_3)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_9.addWidget(self.label_3)

        self.userChangeEdit = QLineEdit(self.tab_3)
        self.userChangeEdit.setObjectName(u"userChangeEdit")

        self.horizontalLayout_9.addWidget(self.userChangeEdit)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_9 = QLabel(self.tab_3)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_11.addWidget(self.label_9)

        self.passwordChangeEdit = QLineEdit(self.tab_3)
        self.passwordChangeEdit.setObjectName(u"passwordChangeEdit")

        self.horizontalLayout_11.addWidget(self.passwordChangeEdit)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(self.tab_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)

        self.newPasswordEdit = QLineEdit(self.tab_3)
        self.newPasswordEdit.setObjectName(u"newPasswordEdit")

        self.horizontalLayout_7.addWidget(self.newPasswordEdit)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.verfyButton = QPushButton(self.tab_3)
        self.verfyButton.setObjectName(u"verfyButton")

        self.verticalLayout_6.addWidget(self.verfyButton)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_4)


        self.horizontalLayout_8.addLayout(self.verticalLayout_6)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_9 = QVBoxLayout(self.tab_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.commandLinkButton_3 = QCommandLinkButton(self.tab_4)
        self.commandLinkButton_3.setObjectName(u"commandLinkButton_3")

        self.verticalLayout_14.addWidget(self.commandLinkButton_3)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_9)


        self.horizontalLayout_14.addLayout(self.verticalLayout_14)

        self.scrollArea_3 = SmoothScrollArea(self.tab_4)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 569, 3253))
        self.verticalLayout_10 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.proxy_0 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioProxyGroup = QButtonGroup(LoginNew)
        self.radioProxyGroup.setObjectName(u"radioProxyGroup")
        self.radioProxyGroup.addButton(self.proxy_0)
        self.proxy_0.setObjectName(u"proxy_0")

        self.horizontalLayout_15.addWidget(self.proxy_0)


        self.verticalLayout_10.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.proxy_1 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioProxyGroup.addButton(self.proxy_1)
        self.proxy_1.setObjectName(u"proxy_1")
        self.proxy_1.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_16.addWidget(self.proxy_1)

        self.line_4 = QFrame(self.scrollAreaWidgetContents_3)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_16.addWidget(self.line_4)

        self.label_13 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_16.addWidget(self.label_13)

        self.httpLine = QLineEdit(self.scrollAreaWidgetContents_3)
        self.httpLine.setObjectName(u"httpLine")

        self.horizontalLayout_16.addWidget(self.httpLine)


        self.verticalLayout_10.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.proxy_2 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioProxyGroup.addButton(self.proxy_2)
        self.proxy_2.setObjectName(u"proxy_2")
        self.proxy_2.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_17.addWidget(self.proxy_2)

        self.line_5 = QFrame(self.scrollAreaWidgetContents_3)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_17.addWidget(self.line_5)

        self.label_14 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_17.addWidget(self.label_14)

        self.sockEdit = QLineEdit(self.scrollAreaWidgetContents_3)
        self.sockEdit.setObjectName(u"sockEdit")

        self.horizontalLayout_17.addWidget(self.sockEdit)


        self.verticalLayout_10.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.proxy_3 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioProxyGroup.addButton(self.proxy_3)
        self.proxy_3.setObjectName(u"proxy_3")

        self.horizontalLayout_18.addWidget(self.proxy_3)

        self.checkLabel = QLabel(self.scrollAreaWidgetContents_3)
        self.checkLabel.setObjectName(u"checkLabel")
        font = QFont()
        font.setBold(False)
        self.checkLabel.setFont(font)
        self.checkLabel.setStyleSheet(u"color:rgb(255, 0, 0)")

        self.horizontalLayout_18.addWidget(self.checkLabel)

        self.proxyLabel = QLabel(self.scrollAreaWidgetContents_3)
        self.proxyLabel.setObjectName(u"proxyLabel")

        self.horizontalLayout_18.addWidget(self.proxyLabel)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_7)


        self.verticalLayout_10.addLayout(self.horizontalLayout_18)

        self.line_6 = QFrame(self.scrollAreaWidgetContents_3)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_10.addWidget(self.line_6)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_15 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_20.addWidget(self.label_15)

        self.apiTimeout = WheelComboBox(self.scrollAreaWidgetContents_3)
        self.apiTimeout.addItem("")
        self.apiTimeout.addItem("")
        self.apiTimeout.addItem("")
        self.apiTimeout.setObjectName(u"apiTimeout")

        self.horizontalLayout_20.addWidget(self.apiTimeout)

        self.label_16 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_20.addWidget(self.label_16)

        self.imgTimeout = WheelComboBox(self.scrollAreaWidgetContents_3)
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.setObjectName(u"imgTimeout")

        self.horizontalLayout_20.addWidget(self.imgTimeout)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_8)


        self.verticalLayout_10.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_9)


        self.verticalLayout_10.addLayout(self.horizontalLayout_21)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")

        self.verticalLayout_10.addLayout(self.verticalLayout_11)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.echBox = QCheckBox(self.scrollAreaWidgetContents_3)
        self.echBox.setObjectName(u"echBox")
        self.echBox.setChecked(True)

        self.horizontalLayout_22.addWidget(self.echBox)

        self.echTick = QLabel(self.scrollAreaWidgetContents_3)
        self.echTick.setObjectName(u"echTick")

        self.horizontalLayout_22.addWidget(self.echTick)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_10)


        self.verticalLayout_10.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")

        self.verticalLayout_10.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_17 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_24.addWidget(self.label_17)

        self.dohLine = TipLineEdit(self.scrollAreaWidgetContents_3)
        self.dohLine.setObjectName(u"dohLine")

        self.horizontalLayout_24.addWidget(self.dohLine)

        self.dohTool = QToolButton(self.scrollAreaWidgetContents_3)
        self.dohTool.setObjectName(u"dohTool")

        self.horizontalLayout_24.addWidget(self.dohTool)


        self.verticalLayout_10.addLayout(self.horizontalLayout_24)

        self.line_8 = QFrame(self.scrollAreaWidgetContents_3)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_10.addWidget(self.line_8)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")

        self.verticalLayout_10.addLayout(self.horizontalLayout_25)

        self.testSpeedButton = QPushButton(self.scrollAreaWidgetContents_3)
        self.testSpeedButton.setObjectName(u"testSpeedButton")

        self.verticalLayout_10.addWidget(self.testSpeedButton)

        self.line_7 = QFrame(self.scrollAreaWidgetContents_3)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_10.addWidget(self.line_7)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_20 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_20, 1, 1, 1, 1)

        self.label_19 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_19, 1, 3, 1, 1)

        self.radioButton_3 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioApiGroup = QButtonGroup(LoginNew)
        self.radioApiGroup.setObjectName(u"radioApiGroup")
        self.radioApiGroup.addButton(self.radioButton_3)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.gridLayout_2.addWidget(self.radioButton_3, 4, 0, 1, 1)

        self.label_img_6 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_img_6.setObjectName(u"label_img_6")

        self.gridLayout_2.addWidget(self.label_img_6, 6, 3, 1, 1)

        self.label_api_2 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_api_2.setObjectName(u"label_api_2")

        self.gridLayout_2.addWidget(self.label_api_2, 3, 1, 1, 1)

        self.radio_img_5 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioImgGroup = QButtonGroup(LoginNew)
        self.radioImgGroup.setObjectName(u"radioImgGroup")
        self.radioImgGroup.addButton(self.radio_img_5)
        self.radio_img_5.setObjectName(u"radio_img_5")

        self.gridLayout_2.addWidget(self.radio_img_5, 5, 2, 1, 1)

        self.radio_img_6 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioImgGroup.addButton(self.radio_img_6)
        self.radio_img_6.setObjectName(u"radio_img_6")

        self.gridLayout_2.addWidget(self.radio_img_6, 6, 2, 1, 1)

        self.radio_img_2 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioImgGroup.addButton(self.radio_img_2)
        self.radio_img_2.setObjectName(u"radio_img_2")

        self.gridLayout_2.addWidget(self.radio_img_2, 3, 2, 1, 1)

        self.radioButton_5 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioApiGroup.addButton(self.radioButton_5)
        self.radioButton_5.setObjectName(u"radioButton_5")

        self.gridLayout_2.addWidget(self.radioButton_5, 5, 0, 1, 1)

        self.radioButton_6 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioApiGroup.addButton(self.radioButton_6)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.gridLayout_2.addWidget(self.radioButton_6, 6, 0, 1, 1)

        self.radio_img_1 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioImgGroup.addButton(self.radio_img_1)
        self.radio_img_1.setObjectName(u"radio_img_1")
        self.radio_img_1.setChecked(False)

        self.gridLayout_2.addWidget(self.radio_img_1, 2, 2, 1, 1)

        self.label_18 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_18, 1, 0, 1, 1)

        self.radioButton_2 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioApiGroup.addButton(self.radioButton_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_2.addWidget(self.radioButton_2, 3, 0, 1, 1)

        self.label_api_3 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_api_3.setObjectName(u"label_api_3")

        self.gridLayout_2.addWidget(self.label_api_3, 4, 1, 1, 1)

        self.label_img_1 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_img_1.setObjectName(u"label_img_1")

        self.gridLayout_2.addWidget(self.label_img_1, 2, 3, 1, 1)

        self.label_api_1 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_api_1.setObjectName(u"label_api_1")

        self.gridLayout_2.addWidget(self.label_api_1, 2, 1, 1, 1)

        self.label_img_5 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_img_5.setObjectName(u"label_img_5")

        self.gridLayout_2.addWidget(self.label_img_5, 5, 3, 1, 1)

        self.radioButton_1 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioApiGroup.addButton(self.radioButton_1)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_1, 2, 0, 1, 1)

        self.label_api_6 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_api_6.setObjectName(u"label_api_6")

        self.gridLayout_2.addWidget(self.label_api_6, 6, 1, 1, 1)

        self.radio_img_3 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioImgGroup.addButton(self.radio_img_3)
        self.radio_img_3.setObjectName(u"radio_img_3")

        self.gridLayout_2.addWidget(self.radio_img_3, 4, 2, 1, 1)

        self.label_21 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_21, 1, 2, 1, 1)

        self.label_img_3 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_img_3.setObjectName(u"label_img_3")

        self.gridLayout_2.addWidget(self.label_img_3, 4, 3, 1, 1)

        self.label_img_2 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_img_2.setObjectName(u"label_img_2")

        self.gridLayout_2.addWidget(self.label_img_2, 3, 3, 1, 1)

        self.label_api_5 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_api_5.setObjectName(u"label_api_5")

        self.gridLayout_2.addWidget(self.label_api_5, 5, 1, 1, 1)


        self.verticalLayout_10.addLayout(self.gridLayout_2)

        self.line_9 = QFrame(self.scrollAreaWidgetContents_3)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.HLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_10.addWidget(self.line_9)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_api_4 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_api_4.setObjectName(u"label_api_4")

        self.gridLayout.addWidget(self.label_api_4, 0, 1, 1, 1)

        self.label_img_4 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_img_4.setObjectName(u"label_img_4")

        self.gridLayout.addWidget(self.label_img_4, 0, 3, 1, 1)

        self.radioButton_4 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioApiGroup.addButton(self.radioButton_4)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.gridLayout.addWidget(self.radioButton_4, 0, 0, 1, 1)

        self.radio_img_4 = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radioImgGroup.addButton(self.radio_img_4)
        self.radio_img_4.setObjectName(u"radio_img_4")

        self.gridLayout.addWidget(self.radio_img_4, 0, 2, 1, 1)


        self.verticalLayout_10.addLayout(self.gridLayout)

        self.testIpButton = QPushButton(self.scrollAreaWidgetContents_3)
        self.testIpButton.setObjectName(u"testIpButton")

        self.verticalLayout_10.addWidget(self.testIpButton)

        self.line_10 = QFrame(self.scrollAreaWidgetContents_3)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.HLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_10.addWidget(self.line_10)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_25 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setStyleSheet(u"color:rgb(255, 0, 0)")

        self.verticalLayout_2.addWidget(self.label_25)


        self.verticalLayout_10.addLayout(self.verticalLayout_2)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_2 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_29.addWidget(self.label_2)

        self.proxyIpEdit = TipLineEdit(self.scrollAreaWidgetContents_3)
        self.proxyIpEdit.setObjectName(u"proxyIpEdit")
        self.proxyIpEdit.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_29.addWidget(self.proxyIpEdit)

        self.proxyIpLabel = QLabel(self.scrollAreaWidgetContents_3)
        self.proxyIpLabel.setObjectName(u"proxyIpLabel")
        self.proxyIpLabel.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_29.addWidget(self.proxyIpLabel)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_11)


        self.verticalLayout_10.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_22 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_26.addWidget(self.label_22)

        self.ipListEdit = QLineEdit(self.scrollAreaWidgetContents_3)
        self.ipListEdit.setObjectName(u"ipListEdit")

        self.horizontalLayout_26.addWidget(self.ipListEdit)


        self.verticalLayout_10.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.line_11 = QFrame(self.scrollAreaWidgetContents_3)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.VLine)
        self.line_11.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_28.addWidget(self.line_11)


        self.verticalLayout_10.addLayout(self.horizontalLayout_28)

        self.tableWidget = BaseTableWidget(self.scrollAreaWidgetContents_3)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(0, 2560))

        self.verticalLayout_10.addWidget(self.tableWidget)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_24 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_27.addWidget(self.label_24)

        self.cdnLinkButton = QCommandLinkButton(self.scrollAreaWidgetContents_3)
        self.cdnLinkButton.setObjectName(u"cdnLinkButton")

        self.horizontalLayout_27.addWidget(self.cdnLinkButton)


        self.verticalLayout_10.addLayout(self.horizontalLayout_27)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.horizontalLayout_14.addWidget(self.scrollArea_3)


        self.verticalLayout_9.addLayout(self.horizontalLayout_14)

        self.tabWidget.addTab(self.tab_4, "")

        self.horizontalLayout_3.addWidget(self.tabWidget)

        QWidget.setTabOrder(self.userEdit_2, self.passwdEdit_2)
        QWidget.setTabOrder(self.passwdEdit_2, self.loginButton)
        QWidget.setTabOrder(self.loginButton, self.proxyIpEdit)
        QWidget.setTabOrder(self.proxyIpEdit, self.autoSign)
        QWidget.setTabOrder(self.autoSign, self.testIpButton)
        QWidget.setTabOrder(self.testIpButton, self.ipListEdit)
        QWidget.setTabOrder(self.ipListEdit, self.scrollArea_4)
        QWidget.setTabOrder(self.scrollArea_4, self.answer1Edit)
        QWidget.setTabOrder(self.answer1Edit, self.answer3Edit)
        QWidget.setTabOrder(self.answer3Edit, self.passwdEdit)
        QWidget.setTabOrder(self.passwdEdit, self.nameEdit)
        QWidget.setTabOrder(self.nameEdit, self.userEdit)
        QWidget.setTabOrder(self.userEdit, self.question3Edit)
        QWidget.setTabOrder(self.question3Edit, self.birthdayEdit)
        QWidget.setTabOrder(self.birthdayEdit, self.answer2Edit)
        QWidget.setTabOrder(self.answer2Edit, self.question1Edit)
        QWidget.setTabOrder(self.question1Edit, self.question2Edit)
        QWidget.setTabOrder(self.question2Edit, self.gender_m)
        QWidget.setTabOrder(self.gender_m, self.gender_f)
        QWidget.setTabOrder(self.gender_f, self.gender_bot)
        QWidget.setTabOrder(self.gender_bot, self.registerButton)
        QWidget.setTabOrder(self.registerButton, self.userChangeEdit)
        QWidget.setTabOrder(self.userChangeEdit, self.passwordChangeEdit)
        QWidget.setTabOrder(self.passwordChangeEdit, self.newPasswordEdit)
        QWidget.setTabOrder(self.newPasswordEdit, self.verfyButton)
        QWidget.setTabOrder(self.verfyButton, self.commandLinkButton_3)
        QWidget.setTabOrder(self.commandLinkButton_3, self.scrollArea_3)
        QWidget.setTabOrder(self.scrollArea_3, self.proxy_0)
        QWidget.setTabOrder(self.proxy_0, self.proxy_1)
        QWidget.setTabOrder(self.proxy_1, self.httpLine)
        QWidget.setTabOrder(self.httpLine, self.proxy_2)
        QWidget.setTabOrder(self.proxy_2, self.sockEdit)
        QWidget.setTabOrder(self.sockEdit, self.proxy_3)
        QWidget.setTabOrder(self.proxy_3, self.apiTimeout)
        QWidget.setTabOrder(self.apiTimeout, self.imgTimeout)
        QWidget.setTabOrder(self.imgTimeout, self.echBox)
        QWidget.setTabOrder(self.echBox, self.dohLine)
        QWidget.setTabOrder(self.dohLine, self.dohTool)
        QWidget.setTabOrder(self.dohTool, self.testSpeedButton)
        QWidget.setTabOrder(self.testSpeedButton, self.radioButton_3)
        QWidget.setTabOrder(self.radioButton_3, self.radio_img_5)
        QWidget.setTabOrder(self.radio_img_5, self.radio_img_6)
        QWidget.setTabOrder(self.radio_img_6, self.radio_img_2)
        QWidget.setTabOrder(self.radio_img_2, self.radioButton_5)
        QWidget.setTabOrder(self.radioButton_5, self.radioButton_6)
        QWidget.setTabOrder(self.radioButton_6, self.radio_img_1)
        QWidget.setTabOrder(self.radio_img_1, self.radioButton_2)
        QWidget.setTabOrder(self.radioButton_2, self.radioButton_1)
        QWidget.setTabOrder(self.radioButton_1, self.radio_img_3)
        QWidget.setTabOrder(self.radio_img_3, self.radioButton_4)
        QWidget.setTabOrder(self.radioButton_4, self.radio_img_4)
        QWidget.setTabOrder(self.radio_img_4, self.saveBox)
        QWidget.setTabOrder(self.saveBox, self.autoBox)
        QWidget.setTabOrder(self.autoBox, self.tableWidget)
        QWidget.setTabOrder(self.tableWidget, self.cdnLinkButton)
        QWidget.setTabOrder(self.cdnLinkButton, self.tabWidget)

        self.retranslateUi(LoginNew)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(LoginNew)
    # setupUi

    def retranslateUi(self, LoginNew):
        LoginNew.setWindowTitle(QCoreApplication.translate("LoginNew", u"\u767b\u5f55", None))
        self.label_5.setText(QCoreApplication.translate("LoginNew", u"\u7528\u6237\u540d", None))
        self.label_6.setText(QCoreApplication.translate("LoginNew", u"\u5bc6\u7801", None))
        self.saveBox.setText(QCoreApplication.translate("LoginNew", u"\u4fdd\u5b58\u5bc6\u7801", None))
        self.autoBox.setText(QCoreApplication.translate("LoginNew", u"\u81ea\u52a8\u767b\u5f55", None))
        self.autoSign.setText(QCoreApplication.translate("LoginNew", u"\u81ea\u52a8\u6253\u5361", None))
        self.loginButton.setText(QCoreApplication.translate("LoginNew", u"\u767b\u5f55", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("LoginNew", u"\u767b\u5f55", None))
        self.answer1.setText(QCoreApplication.translate("LoginNew", u"\u7b54\u68481\uff1a", None))
        self.answer3.setText(QCoreApplication.translate("LoginNew", u"\u7b54\u68483\uff1a", None))
        self.passwd.setText(QCoreApplication.translate("LoginNew", u"\u5bc6\u7801\uff1a", None))
        self.name.setText(QCoreApplication.translate("LoginNew", u"\u540d\u79f0\uff1a", None))
        self.user.setText(QCoreApplication.translate("LoginNew", u"\u8d26\u53f7\uff1a", None))
        self.question3.setText(QCoreApplication.translate("LoginNew", u"\u95ee\u98983\uff1a", None))
        self.birthday.setText(QCoreApplication.translate("LoginNew", u"\u751f\u65e5\uff1a", None))
        self.answer2.setText(QCoreApplication.translate("LoginNew", u"\u7b54\u68482\uff1a", None))
        self.question1.setText(QCoreApplication.translate("LoginNew", u"\u95ee\u98981\uff1a", None))
        self.question2.setText(QCoreApplication.translate("LoginNew", u"\u95ee\u98982\uff1a", None))
        self.gender_m.setText(QCoreApplication.translate("LoginNew", u"\u7537", None))
        self.gender_f.setText(QCoreApplication.translate("LoginNew", u"\u5973", None))
        self.gender_bot.setText(QCoreApplication.translate("LoginNew", u"\u53cc\u6027", None))
        self.registerButton.setText(QCoreApplication.translate("LoginNew", u"\u6ce8\u518c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("LoginNew", u"\u6ce8\u518c", None))
        self.label_3.setText(QCoreApplication.translate("LoginNew", u"\u7528\u6237\u540d\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("LoginNew", u"\u5bc6    \u7801\uff1a", None))
        self.label.setText(QCoreApplication.translate("LoginNew", u"\u65b0\u5bc6\u7801\uff1a", None))
        self.verfyButton.setText(QCoreApplication.translate("LoginNew", u"\u53d1\u9001", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("LoginNew", u"\u4fee\u6539\u5bc6\u7801", None))
        self.commandLinkButton_3.setText(QCoreApplication.translate("LoginNew", u"\u5206\u6d41", None))
        self.proxy_0.setText(QCoreApplication.translate("LoginNew", u"\u65e0\u4ee3\u7406", None))
        self.proxy_1.setText(QCoreApplication.translate("LoginNew", u"HTTP\u4ee3\u7406", None))
        self.label_13.setText(QCoreApplication.translate("LoginNew", u"\u4ee3\u7406\u5730\u5740", None))
#if QT_CONFIG(tooltip)
        self.httpLine.setToolTip(QCoreApplication.translate("LoginNew", u"http://127.0.0.1:10809", None))
#endif // QT_CONFIG(tooltip)
        self.httpLine.setPlaceholderText("")
        self.proxy_2.setText(QCoreApplication.translate("LoginNew", u"Sock5\u4ee3\u7406", None))
        self.label_14.setText(QCoreApplication.translate("LoginNew", u"\u4ee3\u7406\u5730\u5740", None))
#if QT_CONFIG(tooltip)
        self.sockEdit.setToolTip(QCoreApplication.translate("LoginNew", u"127.0.0.1:10808", None))
#endif // QT_CONFIG(tooltip)
        self.sockEdit.setPlaceholderText("")
        self.proxy_3.setText(QCoreApplication.translate("LoginNew", u"\u4f7f\u7528\u7cfb\u7edf\u4ee3\u7406", None))
        self.checkLabel.setText(QCoreApplication.translate("LoginNew", u"\u672a\u68c0\u6d4b\u5230\u7cfb\u7edf\u4ee3\u7406", None))
        self.proxyLabel.setText("")
        self.label_15.setText(QCoreApplication.translate("LoginNew", u"API\u8d85\u65f6\u65f6\u95f4  ", None))
        self.apiTimeout.setItemText(0, QCoreApplication.translate("LoginNew", u"2", None))
        self.apiTimeout.setItemText(1, QCoreApplication.translate("LoginNew", u"5", None))
        self.apiTimeout.setItemText(2, QCoreApplication.translate("LoginNew", u"7", None))

        self.label_16.setText(QCoreApplication.translate("LoginNew", u"\u56fe\u7247\u8d85\u65f6\u65f6\u95f4 ", None))
        self.imgTimeout.setItemText(0, QCoreApplication.translate("LoginNew", u"2", None))
        self.imgTimeout.setItemText(1, QCoreApplication.translate("LoginNew", u"5", None))
        self.imgTimeout.setItemText(2, QCoreApplication.translate("LoginNew", u"7", None))
        self.imgTimeout.setItemText(3, QCoreApplication.translate("LoginNew", u"10", None))
        self.imgTimeout.setItemText(4, QCoreApplication.translate("LoginNew", u"15", None))

        self.echBox.setText(QCoreApplication.translate("LoginNew", u"\u542f\u7528ECH\uff08Encrypted Client Hello\uff09", None))
        self.echTick.setText("")
        self.label_17.setText(QCoreApplication.translate("LoginNew", u"DOH\u5730\u5740\uff1a", None))
        self.dohTool.setText("")
        self.testSpeedButton.setText(QCoreApplication.translate("LoginNew", u"\u6d4b\u901f", None))
        self.label_20.setText(QCoreApplication.translate("LoginNew", u"\u5ef6\u8fdf", None))
        self.label_19.setText(QCoreApplication.translate("LoginNew", u"\u901f\u5ea6", None))
        self.radioButton_3.setText(QCoreApplication.translate("LoginNew", u"\u5206\u6d413", None))
        self.label_img_6.setText("")
        self.label_api_2.setText("")
#if QT_CONFIG(tooltip)
        self.radio_img_5.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.radio_img_5.setText(QCoreApplication.translate("LoginNew", u"JP\u53cd\u4ee3\u5206\u6d41", None))
        self.radio_img_6.setText(QCoreApplication.translate("LoginNew", u"US\u53cd\u4ee3\u5206\u6d41", None))
        self.radio_img_2.setText(QCoreApplication.translate("LoginNew", u"\u5206\u6d412", None))
#if QT_CONFIG(tooltip)
        self.radioButton_5.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.radioButton_5.setText(QCoreApplication.translate("LoginNew", u"JP\u53cd\u4ee3\u5206\u6d41", None))
        self.radioButton_6.setText(QCoreApplication.translate("LoginNew", u"US\u53cd\u4ee3\u5206\u6d41", None))
        self.radio_img_1.setText(QCoreApplication.translate("LoginNew", u"\u5206\u6d411", None))
        self.label_18.setText(QCoreApplication.translate("LoginNew", u"Api\u5206\u6d41", None))
        self.radioButton_2.setText(QCoreApplication.translate("LoginNew", u"\u5206\u6d412", None))
        self.label_api_3.setText("")
        self.label_img_1.setText("")
        self.label_api_1.setText("")
        self.label_img_5.setText("")
        self.radioButton_1.setText(QCoreApplication.translate("LoginNew", u"\u5206\u6d411", None))
        self.label_api_6.setText("")
        self.radio_img_3.setText(QCoreApplication.translate("LoginNew", u"\u5206\u6d413", None))
        self.label_21.setText(QCoreApplication.translate("LoginNew", u"\u56fe\u7247\u5206\u6d41", None))
        self.label_img_3.setText("")
        self.label_img_2.setText("")
        self.label_api_5.setText("")
        self.label_api_4.setText("")
        self.label_img_4.setText("")
        self.radioButton_4.setText(QCoreApplication.translate("LoginNew", u"IP\u5206\u6d41", None))
        self.radio_img_4.setText(QCoreApplication.translate("LoginNew", u"IP\u5206\u6d41", None))
        self.testIpButton.setText(QCoreApplication.translate("LoginNew", u"\u6d4b\u8bd5IP\u5206\u6d41", None))
        self.label_25.setText(QCoreApplication.translate("LoginNew", u"*\u4f7f\u7528\u4ee3\u7406\u65f6IP\u5206\u6d41\u4e0d\u751f\u6548\uff0c\u63a8\u8350\u5f00\u542fECH\u529f\u80fd", None))
        self.label_2.setText(QCoreApplication.translate("LoginNew", u"\u81ea\u5b9a\u4e49\u83b7\u53d6ProxyIP\u5730\u533a\uff1a", None))
        self.proxyIpLabel.setText("")
        self.label_22.setText(QCoreApplication.translate("LoginNew", u"\u81ea\u5b9a\u4e49IP\u5217\u8868\uff08\u9017\u53f7\u5206\u5272\uff09\uff1a", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("LoginNew", u"\u540d\u79f0", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("LoginNew", u"IP", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("LoginNew", u"\u5730\u533a", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("LoginNew", u"ISP", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("LoginNew", u"\u901f\u5ea6", None));
        self.label_24.setText(QCoreApplication.translate("LoginNew", u"\u5206\u6d41\u8bbe\u7f6e\u8bf7\u770b\u8bf4\u660e\u83b7\u53d6", None))
        self.cdnLinkButton.setText(QCoreApplication.translate("LoginNew", u"\u8bf4\u660e", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("LoginNew", u"\u5206\u6d41", None))
    # retranslateUi

