# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_change_password_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ChangePasswordWidget(object):
    def setupUi(self, ChangePasswordWidget):
        if not ChangePasswordWidget.objectName():
            ChangePasswordWidget.setObjectName(u"ChangePasswordWidget")
        ChangePasswordWidget.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(ChangePasswordWidget)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.label_5 = QLabel(ChangePasswordWidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.userEdit = QLineEdit(ChangePasswordWidget)
        self.userEdit.setObjectName(u"userEdit")

        self.verticalLayout_2.addWidget(self.userEdit)

        self.label_6 = QLabel(ChangePasswordWidget)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.passwordEdit = QLineEdit(ChangePasswordWidget)
        self.passwordEdit.setObjectName(u"passwordEdit")
        self.passwordEdit.setEchoMode(QLineEdit.Normal)

        self.verticalLayout_2.addWidget(self.passwordEdit)

        self.label = QLabel(ChangePasswordWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.newPasswordEdit = QLineEdit(ChangePasswordWidget)
        self.newPasswordEdit.setObjectName(u"newPasswordEdit")

        self.verticalLayout_2.addWidget(self.newPasswordEdit)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.retranslateUi(ChangePasswordWidget)

        QMetaObject.connectSlotsByName(ChangePasswordWidget)
    # setupUi

    def retranslateUi(self, ChangePasswordWidget):
        ChangePasswordWidget.setWindowTitle(QCoreApplication.translate("ChangePasswordWidget", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("ChangePasswordWidget", u"\u7528\u6237\u540d", None))
        self.label_6.setText(QCoreApplication.translate("ChangePasswordWidget", u"\u5bc6\u7801", None))
        self.label.setText(QCoreApplication.translate("ChangePasswordWidget", u"\u65b0\u5bc6\u7801", None))
    # retranslateUi

