# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_search_item.ui'
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
    QWidget)

class Ui_SearchItem(object):
    def setupUi(self, SearchItem):
        if not SearchItem.objectName():
            SearchItem.setObjectName(u"SearchItem")
        SearchItem.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(SearchItem)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(SearchItem)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label, 0, Qt.AlignLeft)

        self.widget = QWidget(SearchItem)
        self.widget.setObjectName(u"widget")

        self.horizontalLayout.addWidget(self.widget, 0, Qt.AlignRight)


        self.retranslateUi(SearchItem)

        QMetaObject.connectSlotsByName(SearchItem)
    # setupUi

    def retranslateUi(self, SearchItem):
        SearchItem.setWindowTitle(QCoreApplication.translate("SearchItem", u"Form", None))
        self.label.setText(QCoreApplication.translate("SearchItem", u"TextLabel", None))
    # retranslateUi

