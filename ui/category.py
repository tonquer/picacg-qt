# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'category.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QListWidgetItem, QSizePolicy,
    QWidget)

from .qtlistwidget import QtBookList

class Ui_category(object):
    def setupUi(self, category):
        if not category.objectName():
            category.setObjectName(u"category")
        category.resize(400, 300)
        self.gridLayout_2 = QGridLayout(category)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.bookList = QtBookList(category)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.gridLayout_2.addWidget(self.bookList, 0, 0, 1, 1)


        self.retranslateUi(category)

        QMetaObject.connectSlotsByName(category)
    # setupUi

    def retranslateUi(self, category):
        category.setWindowTitle(QCoreApplication.translate("category", u"Form", None))
    # retranslateUi

