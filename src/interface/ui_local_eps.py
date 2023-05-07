# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_local_eps.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QListWidgetItem, QSizePolicy,
    QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_LocalEps(object):
    def setupUi(self, LocalEps):
        if not LocalEps.objectName():
            LocalEps.setObjectName(u"LocalEps")
        LocalEps.resize(646, 391)
        self.gridLayout_2 = QGridLayout(LocalEps)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bookList = ComicListWidget(LocalEps)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)


        self.retranslateUi(LocalEps)

        QMetaObject.connectSlotsByName(LocalEps)
    # setupUi

    def retranslateUi(self, LocalEps):
        LocalEps.setWindowTitle(QCoreApplication.translate("LocalEps", u"\u672c\u5730\u6f2b\u753b\u7ae0\u8282", None))
    # retranslateUi

