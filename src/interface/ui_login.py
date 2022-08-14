# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_login.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QPushButton,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

from view.user.change_password_widget import ChangePasswordWidget
from view.user.login_proxy_widget import LoginProxyWidget
from view.user.login_widget import LoginWidget
from view.user.register_widget import RegisterWidget

class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(350, 305)
        Login.setMinimumSize(QSize(350, 0))
        Login.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_2 = QVBoxLayout(Login)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.tabWidget = QTabWidget(Login)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = LoginWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_3 = QVBoxLayout(self.tab)
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 9, 9, 9)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = RegisterWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = ChangePasswordWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_3 = LoginProxyWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.loginButton = QPushButton(Login)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setMaximumSize(QSize(150, 30))
        self.loginButton.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.loginButton)

        self.closeButton = QPushButton(Login)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMaximumSize(QSize(150, 30))

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Login)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Dialog", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Login", u"\u767b\u5f55", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Login", u"\u6ce8\u518c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Login", u"\u4fee\u6539\u5bc6\u7801", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Login", u"\u5206\u6d41", None))
        self.loginButton.setText(QCoreApplication.translate("Login", u"\u786e\u5b9a", None))
#if QT_CONFIG(shortcut)
        self.loginButton.setShortcut(QCoreApplication.translate("Login", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.closeButton.setText(QCoreApplication.translate("Login", u"\u5173\u95ed", None))
    # retranslateUi

