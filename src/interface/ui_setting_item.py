# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_setting_item.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_SettingItem(object):
    def setupUi(self, SettingItem):
        if not SettingItem.objectName():
            SettingItem.setObjectName(u"SettingItem")
        SettingItem.resize(400, 300)
        SettingItem.setStyleSheet(u"QWidget#SettingItem\n"
"{\n"
"	\n"
"	background-color: rgb(253, 253, 253);\n"
"	border: 3px solid rgb(229, 229, 229);\n"
"}\n"
"QWidget#widget\n"
"{\n"
"	\n"
"	background-color: rgb(247, 247, 247);\n"
"	border: 3px solid rgb(229, 229, 229);\n"
"}")
        self.verticalLayout = QVBoxLayout(SettingItem)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(SettingItem)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(SettingItem)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(SettingItem)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.label_4 = QLabel(SettingItem)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.toolButton = QToolButton(SettingItem)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setArrowType(Qt.UpArrow)

        self.horizontalLayout.addWidget(self.toolButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.widget = QWidget(SettingItem)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(SettingItem)

        QMetaObject.connectSlotsByName(SettingItem)
    # setupUi

    def retranslateUi(self, SettingItem):
        SettingItem.setWindowTitle(QCoreApplication.translate("SettingItem", u"Form", None))
        self.label.setText(QCoreApplication.translate("SettingItem", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("SettingItem", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("SettingItem", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("SettingItem", u"TextLabel", None))
        self.toolButton.setText(QCoreApplication.translate("SettingItem", u"...", None))
    # retranslateUi

