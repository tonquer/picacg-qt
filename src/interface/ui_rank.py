# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_rank.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

from component.list.comic_list_widget import ComicListWidget
from component.list.user_list_widget import UserListWidget

class Ui_Rank(object):
    def setupUi(self, Rank):
        if not Rank.objectName():
            Rank.setObjectName(u"Rank")
        Rank.resize(536, 379)
        self.verticalLayout = QVBoxLayout(Rank)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Rank)
        self.tabWidget.setObjectName(u"tabWidget")
        self.widget_1 = QWidget()
        self.widget_1.setObjectName(u"widget_1")
        self.verticalLayout_2 = QVBoxLayout(self.widget_1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.h24BookList = ComicListWidget(self.widget_1)
        self.h24BookList.setObjectName(u"h24BookList")

        self.verticalLayout_2.addWidget(self.h24BookList)

        self.tabWidget.addTab(self.widget_1, "")
        self.widget_2 = QWidget()
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.d7BookList = ComicListWidget(self.widget_2)
        self.d7BookList.setObjectName(u"d7BookList")

        self.verticalLayout_3.addWidget(self.d7BookList)

        self.tabWidget.addTab(self.widget_2, "")
        self.widget_3 = QWidget()
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_4 = QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.d30BookList = ComicListWidget(self.widget_3)
        self.d30BookList.setObjectName(u"d30BookList")

        self.verticalLayout_4.addWidget(self.d30BookList)

        self.tabWidget.addTab(self.widget_3, "")
        self.widget_4 = QWidget()
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_5 = QVBoxLayout(self.widget_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.kindList = UserListWidget(self.widget_4)
        self.kindList.setObjectName(u"kindList")

        self.verticalLayout_5.addWidget(self.kindList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.widget_4)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.widget_4, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Rank)

        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(Rank)
    # setupUi

    def retranslateUi(self, Rank):
        Rank.setWindowTitle(QCoreApplication.translate("Rank", u"\u6392\u884c\u699c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget_1), QCoreApplication.translate("Rank", u"24\u5c0f\u65f6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget_2), QCoreApplication.translate("Rank", u"7\u5929", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget_3), QCoreApplication.translate("Rank", u"30\u5929", None))
        self.pushButton.setText(QCoreApplication.translate("Rank", u"\u6279\u91cf\u4e0b\u8f7d", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget_4), QCoreApplication.translate("Rank", u"\u9a91\u58eb\u699c", None))
    # retranslateUi

