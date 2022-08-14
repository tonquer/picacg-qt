# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_book_eps.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from component.list.base_list_widget import BaseListWidget

class Ui_BookEps(object):
    def setupUi(self, BookEps):
        if not BookEps.objectName():
            BookEps.setObjectName(u"BookEps")
        BookEps.resize(400, 300)
        self.verticalLayout = QVBoxLayout(BookEps)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nameLabel = QLabel(BookEps)
        self.nameLabel.setObjectName(u"nameLabel")

        self.verticalLayout.addWidget(self.nameLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(BookEps)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.selectButton = QPushButton(BookEps)
        self.selectButton.setObjectName(u"selectButton")

        self.horizontalLayout.addWidget(self.selectButton)

        self.cancleButton = QPushButton(BookEps)
        self.cancleButton.setObjectName(u"cancleButton")

        self.horizontalLayout.addWidget(self.cancleButton)

        self.downloadButton = QPushButton(BookEps)
        self.downloadButton.setObjectName(u"downloadButton")

        self.horizontalLayout.addWidget(self.downloadButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = BaseListWidget(BookEps)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.listWidget)


        self.retranslateUi(BookEps)

        QMetaObject.connectSlotsByName(BookEps)
    # setupUi

    def retranslateUi(self, BookEps):
        BookEps.setWindowTitle(QCoreApplication.translate("BookEps", u"\u7ae0\u8282\u4e0b\u8f7d", None))
        self.nameLabel.setText("")
        self.label.setText(QCoreApplication.translate("BookEps", u"\u7ae0\u8282", None))
        self.selectButton.setText(QCoreApplication.translate("BookEps", u"\u5168\u9009", None))
        self.cancleButton.setText(QCoreApplication.translate("BookEps", u"\u53cd\u9009", None))
        self.downloadButton.setText(QCoreApplication.translate("BookEps", u"\u4e0b\u8f7d", None))
    # retranslateUi

