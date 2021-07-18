# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bookinfo.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .qtlistwidget import QtCategoryList
from .qt_comment_list import QtCommentList


class Ui_BookInfo(object):
    def setupUi(self, BookInfo):
        if not BookInfo.objectName():
            BookInfo.setObjectName(u"BookInfo")
        BookInfo.resize(709, 963)
        self.gridLayout_2 = QGridLayout(BookInfo)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.stackedWidget = QStackedWidget(BookInfo)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_4 = QGridLayout(self.page)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.picture = QLabel(self.page)
        self.picture.setObjectName(u"picture")
        self.picture.setMinimumSize(QSize(240, 320))

        self.horizontalLayout.addWidget(self.picture)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(40, 16777215))
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.label)

        self.title = QLabel(self.page)
        self.title.setObjectName(u"title")
        self.title.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.title)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_6 = QLabel(self.page)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_8.addWidget(self.label_6)

        self.idLabel = QLabel(self.page)
        self.idLabel.setObjectName(u"idLabel")

        self.horizontalLayout_8.addWidget(self.idLabel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 0))
        self.label_2.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_11.addWidget(self.label_2)

        self.autorList = QtCategoryList(self.page)
        self.autorList.setObjectName(u"autorList")
        self.autorList.setMaximumSize(QSize(16777215, 40))
        self.autorList.setStyleSheet(u"background-color:transparent;")
        self.autorList.setFrameShape(QFrame.NoFrame)
        self.autorList.setProperty("showDropIndicator", True)
        self.autorList.setFlow(QListView.LeftToRight)
        self.autorList.setSpacing(10)

        self.horizontalLayout_11.addWidget(self.autorList)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_11)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.page)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(40, 16777215))
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.description = QLabel(self.page)
        self.description.setObjectName(u"description")
        self.description.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_5.addWidget(self.description)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.page)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_6.addWidget(self.label_4)

        self.categoriesList = QtCategoryList(self.page)
        self.categoriesList.setObjectName(u"categoriesList")
        self.categoriesList.setMaximumSize(QSize(16777215, 40))
        self.categoriesList.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
"QListWidget::item {\n"
"    background-color:rgb(251, 239, 243);\n"
"    color: rgb(196, 95, 125);\n"
"	border:2px solid red;\n"
"    border-radius: 10px;\n"
"	border-color:rgb(196, 95, 125);\n"
"}\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QListWidget::item:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"")
        self.categoriesList.setFrameShape(QFrame.NoFrame)
        self.categoriesList.setSpacing(6)

        self.horizontalLayout_6.addWidget(self.categoriesList)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.page)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_7.addWidget(self.label_5)

        self.tagsList = QtCategoryList(self.page)
        self.tagsList.setObjectName(u"tagsList")
        self.tagsList.setMaximumSize(QSize(16777215, 40))
        self.tagsList.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
"QListWidget::item {\n"
"    background-color:rgb(251, 239, 243);\n"
"    color: rgb(196, 95, 125);\n"
"	border:2px solid red;\n"
"    border-radius: 10px;\n"
"	border-color:rgb(196, 95, 125);\n"
"}\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QListWidget::item:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"")
        self.tagsList.setFrameShape(QFrame.NoFrame)
        self.tagsList.setSpacing(6)

        self.horizontalLayout_7.addWidget(self.tagsList)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_7 = QLabel(self.page)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(40, 20))

        self.horizontalLayout_9.addWidget(self.label_7)

        self.views = QLabel(self.page)
        self.views.setObjectName(u"views")
        self.views.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_9.addWidget(self.views)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.updateTick = QLabel(self.page)
        self.updateTick.setObjectName(u"updateTick")
        self.updateTick.setEnabled(True)
        self.updateTick.setMinimumSize(QSize(80, 40))
        self.updateTick.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_2.addWidget(self.updateTick)

        self.starButton = QToolButton(self.page)
        self.starButton.setObjectName(u"starButton")
        self.starButton.setMinimumSize(QSize(40, 40))
        self.starButton.setStyleSheet(u"background-color:transparent;")

        self.horizontalLayout_2.addWidget(self.starButton)

        self.favoriteButton = QToolButton(self.page)
        self.favoriteButton.setObjectName(u"favoriteButton")
        self.favoriteButton.setMinimumSize(QSize(40, 40))
        self.favoriteButton.setStyleSheet(u"background-color:transparent;")

        self.horizontalLayout_2.addWidget(self.favoriteButton)

        self.downloadButton = QToolButton(self.page)
        self.downloadButton.setObjectName(u"downloadButton")
        self.downloadButton.setMinimumSize(QSize(40, 40))
        self.downloadButton.setStyleSheet(u"background-color:transparent;")

        self.horizontalLayout_2.addWidget(self.downloadButton)

        self.startRead = QPushButton(self.page)
        self.startRead.setObjectName(u"startRead")
        self.startRead.setMinimumSize(QSize(0, 40))
        self.startRead.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_2.addWidget(self.startRead)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.tabWidget = QTabWidget(self.page)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"QTabWidget:pane {border-top:0px solid #e8f3f9;background:  transparent; }")
        self.epsWidget = QWidget()
        self.epsWidget.setObjectName(u"epsWidget")
        self.epsLayout = QGridLayout(self.epsWidget)
        self.epsLayout.setObjectName(u"epsLayout")
        self.epsListWidget = QListWidget(self.epsWidget)
        self.epsListWidget.setObjectName(u"epsListWidget")
        self.epsListWidget.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
"QListWidget::item {\n"
"    background-color:rgb(251, 239, 243);\n"
"    color: rgb(196, 95, 125);\n"
"	border:2px solid red;\n"
"    border-radius: 10px;\n"
"	border-color:rgb(196, 95, 125);\n"
"}\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QListWidget::item:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"")
        self.epsListWidget.setTextElideMode(Qt.ElideRight)
        self.epsListWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.epsListWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.epsListWidget.setSpacing(6)

        self.epsLayout.addWidget(self.epsListWidget, 0, 0, 1, 1)

        self.tabWidget.addTab(self.epsWidget, "")
        self.commentWidget = QtCommentList()
        self.commentWidget.setObjectName(u"commentWidget")
        self.commentLayout = QGridLayout(self.commentWidget)
        self.commentLayout.setObjectName(u"commentLayout")
        self.tabWidget.addTab(self.commentWidget, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)

        self.gridLayout_2.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.retranslateUi(BookInfo)
        self.startRead.clicked.connect(BookInfo.StartRead)
        self.starButton.clicked.connect(BookInfo.AddBookLike)
        self.favoriteButton.clicked.connect(BookInfo.AddFavority)
        self.downloadButton.clicked.connect(BookInfo.AddDownload)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(BookInfo)
    # setupUi

    def retranslateUi(self, BookInfo):
        BookInfo.setWindowTitle(QCoreApplication.translate("BookInfo", u"Form", None))
        self.picture.setText(QCoreApplication.translate("BookInfo", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("BookInfo", u"\u6807\u9898\uff1a", None))
        self.title.setText(QCoreApplication.translate("BookInfo", u"\u6807\u9898", None))
        self.label_6.setText(QCoreApplication.translate("BookInfo", u"id:", None))
        self.idLabel.setText("")
        self.label_2.setText(QCoreApplication.translate("BookInfo", u"\u4f5c\u8005\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("BookInfo", u"\u63cf\u8ff0\uff1a", None))
        self.description.setText(QCoreApplication.translate("BookInfo", u"\u63cf\u8ff0", None))
        self.label_4.setText(QCoreApplication.translate("BookInfo", u"\u5206\u7c7b\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("BookInfo", u"Tags\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("BookInfo", u"\u89c2\u770b\u6570\uff1a", None))
        self.views.setText(QCoreApplication.translate("BookInfo", u"\u89c2\u770b\u6570", None))
        self.updateTick.setText(QCoreApplication.translate("BookInfo", u"TextLabel", None))
        self.starButton.setText("")
        self.favoriteButton.setText("")
        self.downloadButton.setText("")
        self.startRead.setText(QCoreApplication.translate("BookInfo", u"\u5f00\u59cb\u9605\u8bfb", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.epsWidget), QCoreApplication.translate("BookInfo", u"\u7ae0\u8282", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.commentWidget), QCoreApplication.translate("BookInfo", u"\u8bc4\u8bba", None))
    # retranslateUi

