# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_setting_item_theme.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
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
from PySide6.QtWidgets import (QApplication, QRadioButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_SettingItemTheme(object):
    def setupUi(self, SettingItemTheme):
        if not SettingItemTheme.objectName():
            SettingItemTheme.setObjectName(u"SettingItemTheme")
        SettingItemTheme.resize(400, 121)
        self.verticalLayout = QVBoxLayout(SettingItemTheme)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radioButton = QRadioButton(SettingItemTheme)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout.addWidget(self.radioButton)


        self.retranslateUi(SettingItemTheme)

        QMetaObject.connectSlotsByName(SettingItemTheme)
    # setupUi

    def retranslateUi(self, SettingItemTheme):
        SettingItemTheme.setWindowTitle(QCoreApplication.translate("SettingItemTheme", u"Form", None))
        self.radioButton.setText(QCoreApplication.translate("SettingItemTheme", u"\u6d45\u8272", None))
    # retranslateUi

