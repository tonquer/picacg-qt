# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_line_edit_help_widget2.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
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
from PySide6.QtWidgets import (QApplication, QLabel, QListView, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_LineEditHelp2(object):
    def setupUi(self, LineEditHelp2):
        if not LineEditHelp2.objectName():
            LineEditHelp2.setObjectName(u"LineEditHelp2")
        LineEditHelp2.resize(400, 440)
        self.verticalLayout_2 = QVBoxLayout(LineEditHelp2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(LineEditHelp2)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.listView = QListView(LineEditHelp2)
        self.listView.setObjectName(u"listView")
        self.listView.setMinimumSize(QSize(0, 120))

        self.verticalLayout_2.addWidget(self.listView)


        self.retranslateUi(LineEditHelp2)

        QMetaObject.connectSlotsByName(LineEditHelp2)
    # setupUi

    def retranslateUi(self, LineEditHelp2):
        LineEditHelp2.setWindowTitle(QCoreApplication.translate("LineEditHelp2", u"Form", None))
        self.label.setText(QCoreApplication.translate("LineEditHelp2", u"\u641c\u7d22\u8bb0\u5f55", None))
    # retranslateUi

