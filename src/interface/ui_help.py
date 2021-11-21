# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_help.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import images_rc

class Ui_Help(object):
    def setupUi(self, Help):
        if not Help.objectName():
            Help.setObjectName(u"Help")
        Help.resize(426, 516)
        self.verticalLayout = QVBoxLayout(Help)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.widget = QWidget(Help)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u":/png/icon/icon_comment.png"))

        self.verticalLayout_2.addWidget(self.label, 0, Qt.AlignHCenter)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2, 0, Qt.AlignHCenter)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3, 0, Qt.AlignHCenter)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_2.addWidget(self.pushButton, 0, Qt.AlignHCenter)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.formLayout = QFormLayout(self.widget_2)
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(self.widget_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.version = QLabel(self.widget_2)
        self.version.setObjectName(u"version")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.version)

        self.label_6 = QLabel(self.widget_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_6)

        self.waifu2x = QLabel(self.widget_2)
        self.waifu2x.setObjectName(u"waifu2x")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.waifu2x)

        self.label_8 = QLabel(self.widget_2)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_8)

        self.local = QLabel(self.widget_2)
        self.local.setObjectName(u"local")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.local)

        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_5)

        self.localNum = QLabel(self.widget_2)
        self.localNum.setObjectName(u"localNum")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.localNum)

        self.label_7 = QLabel(self.widget_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_7)

        self.logButton = QPushButton(self.widget_2)
        self.logButton.setObjectName(u"logButton")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.logButton)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Help)

        QMetaObject.connectSlotsByName(Help)
    # setupUi

    def retranslateUi(self, Help):
        Help.setWindowTitle(QCoreApplication.translate("Help", u"Form", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("Help", u"\u9700\u8981\u53cd\u9988\u4f7f\u7528\u8fc7\u7a0b\u4e2d\u7684\u95ee\u9898\uff1f", None))
        self.label_3.setText(QCoreApplication.translate("Help", u"\u60f3\u63d0\u4f9b\u4e00\u4e9b\u5efa\u8bae\uff1f", None))
        self.pushButton.setText(QCoreApplication.translate("Help", u"Github Issue", None))
        self.label_4.setText(QCoreApplication.translate("Help", u"\u7248\u672c\u53f7:", None))
        self.version.setText(QCoreApplication.translate("Help", u"v1.2.8", None))
        self.label_6.setText(QCoreApplication.translate("Help", u"waifu2x\u7248\u672c:", None))
        self.waifu2x.setText(QCoreApplication.translate("Help", u"v1.0.8", None))
        self.label_8.setText(QCoreApplication.translate("Help", u"\u672c\u5730\u5e93\u7248\u672c:", None))
        self.local.setText("")
        self.label_5.setText(QCoreApplication.translate("Help", u"\u672c\u5730\u5e93\u6570\u91cf:", None))
        self.localNum.setText("")
        self.label_7.setText(QCoreApplication.translate("Help", u"\u65e5\u5fd7:", None))
        self.logButton.setText(QCoreApplication.translate("Help", u"\u6253\u5f00\u65e5\u5fd7\u76ee\u5f55", None))
    # retranslateUi

