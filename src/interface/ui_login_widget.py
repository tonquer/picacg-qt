# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_login_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_LoginWidget(object):
    def setupUi(self, LoginWidget):
        if not LoginWidget.objectName():
            LoginWidget.setObjectName(u"LoginWidget")
        LoginWidget.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(LoginWidget)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.label_2 = QLabel(LoginWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_5 = QLabel(LoginWidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.userEdit_2 = QLineEdit(LoginWidget)
        self.userEdit_2.setObjectName(u"userEdit_2")

        self.verticalLayout_2.addWidget(self.userEdit_2)

        self.label_6 = QLabel(LoginWidget)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.passwdEdit_2 = QLineEdit(LoginWidget)
        self.passwdEdit_2.setObjectName(u"passwdEdit_2")
        self.passwdEdit_2.setEchoMode(QLineEdit.Password)

        self.verticalLayout_2.addWidget(self.passwdEdit_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.saveBox = QCheckBox(LoginWidget)
        self.saveBox.setObjectName(u"saveBox")

        self.horizontalLayout.addWidget(self.saveBox)

        self.autoBox = QCheckBox(LoginWidget)
        self.autoBox.setObjectName(u"autoBox")

        self.horizontalLayout.addWidget(self.autoBox)

        self.autoSign = QCheckBox(LoginWidget)
        self.autoSign.setObjectName(u"autoSign")

        self.horizontalLayout.addWidget(self.autoSign)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.retranslateUi(LoginWidget)

        QMetaObject.connectSlotsByName(LoginWidget)
    # setupUi

    def retranslateUi(self, LoginWidget):
        LoginWidget.setWindowTitle(QCoreApplication.translate("LoginWidget", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("LoginWidget", u"\u5982\u679c\u4e0d\u80fd\u8fde\u63a5\u548c\u770b\u56fe\uff0c\u8bf7\u5c1d\u8bd5\u9009\u62e9\u5176\u4ed6\u5206\u6d41\u3002", None))
        self.label_5.setText(QCoreApplication.translate("LoginWidget", u"\u8d26\u53f7", None))
        self.label_6.setText(QCoreApplication.translate("LoginWidget", u"\u5bc6\u7801", None))
        self.saveBox.setText(QCoreApplication.translate("LoginWidget", u"\u4fdd\u5b58\u5bc6\u7801", None))
        self.autoBox.setText(QCoreApplication.translate("LoginWidget", u"\u81ea\u52a8\u767b\u5f55", None))
        self.autoSign.setText(QCoreApplication.translate("LoginWidget", u"\u81ea\u52a8\u6253\u5361", None))
    # retranslateUi

