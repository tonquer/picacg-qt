# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_nas_item.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_NasItem(object):
    def setupUi(self, NasItem):
        if not NasItem.objectName():
            NasItem.setObjectName(u"NasItem")
        NasItem.resize(514, 147)
        self.verticalLayout = QVBoxLayout(NasItem)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.title = QLabel(NasItem)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.title.setFont(font)

        self.horizontalLayout_2.addWidget(self.title)

        self.editButton = QToolButton(NasItem)
        self.editButton.setObjectName(u"editButton")

        self.horizontalLayout_2.addWidget(self.editButton)

        self.delButton = QToolButton(NasItem)
        self.delButton.setObjectName(u"delButton")

        self.horizontalLayout_2.addWidget(self.delButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.address = QLabel(NasItem)
        self.address.setObjectName(u"address")

        self.horizontalLayout_3.addWidget(self.address)

        self.waifu2x = QLabel(NasItem)
        self.waifu2x.setObjectName(u"waifu2x")

        self.horizontalLayout_3.addWidget(self.waifu2x)

        self.user = QLabel(NasItem)
        self.user.setObjectName(u"user")

        self.horizontalLayout_3.addWidget(self.user)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(NasItem)

        QMetaObject.connectSlotsByName(NasItem)
    # setupUi

    def retranslateUi(self, NasItem):
        NasItem.setWindowTitle(QCoreApplication.translate("NasItem", u"Form", None))
        self.title.setText(QCoreApplication.translate("NasItem", u"\u6d4b\u8bd5", None))
        self.editButton.setText(QCoreApplication.translate("NasItem", u"\u7f16\u8f91", None))
        self.delButton.setText(QCoreApplication.translate("NasItem", u"\u5220\u9664", None))
        self.address.setText("")
        self.waifu2x.setText(QCoreApplication.translate("NasItem", u"waifu2x", None))
        self.user.setText("")
    # retranslateUi

