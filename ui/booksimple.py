# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'booksimple.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_BookSimple(object):
    def setupUi(self, BookSimple):
        if not BookSimple.objectName():
            BookSimple.setObjectName(u"BookSimple")
        BookSimple.resize(725, 500)
        BookSimple.setMinimumSize(QSize(0, 0))
        BookSimple.setStyleSheet(u"background:transparent;border:2px solid red;")
        self.horizontalLayout = QHBoxLayout(BookSimple)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(BookSimple)
        self.title.setObjectName(u"title")

        self.verticalLayout.addWidget(self.title)

        self.autor = QLabel(BookSimple)
        self.autor.setObjectName(u"autor")

        self.verticalLayout.addWidget(self.autor)

        self.category = QLabel(BookSimple)
        self.category.setObjectName(u"category")

        self.verticalLayout.addWidget(self.category)

        self.pushButton = QPushButton(BookSimple)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 0))

        self.verticalLayout.addWidget(self.pushButton)


        self.gridLayout.addLayout(self.verticalLayout, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.picture = QLabel(BookSimple)
        self.picture.setObjectName(u"picture")
        self.picture.setMinimumSize(QSize(240, 480))
        self.picture.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.picture, 1, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.retranslateUi(BookSimple)
        self.pushButton.clicked.connect(BookSimple.OpenBookInfo)

        QMetaObject.connectSlotsByName(BookSimple)
    # setupUi

    def retranslateUi(self, BookSimple):
        BookSimple.setWindowTitle(QCoreApplication.translate("BookSimple", u"Form", None))
        self.title.setText(QCoreApplication.translate("BookSimple", u"TextLabel", None))
        self.autor.setText(QCoreApplication.translate("BookSimple", u"TextLabel", None))
        self.category.setText(QCoreApplication.translate("BookSimple", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("BookSimple", u"\u6253\u5f00", None))
        self.picture.setText(QCoreApplication.translate("BookSimple", u"TextLabel", None))
    # retranslateUi

