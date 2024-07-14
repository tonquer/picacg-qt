# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_book_info.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QCommandLinkButton,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QListView, QListWidgetItem, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QToolButton, QVBoxLayout, QWidget)

from component.button.icon_tool_button import IconToolButton
from component.label.head_label import HeadLabel
from component.list.eps_list_widget import EpsListWidget
from component.list.tag_list_widget import TagListWidget
from component.scroll_area.smooth_scroll_area import SmoothScrollArea
import images_rc
import images_rc

class Ui_BookInfo(object):
    def setupUi(self, BookInfo):
        if not BookInfo.objectName():
            BookInfo.setObjectName(u"BookInfo")
        BookInfo.resize(892, 719)
        BookInfo.setStyleSheet(u"QToolButton\n"
"{\n"
"background-color:transparent;\n"
"  border: 0px;\n"
"  height: 0px;\n"
"  margin: 0px;\n"
"  padding: 0px;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}\n"
"QToolButton:hover  {\n"
"background-color:transparent;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}\n"
"\n"
"QToolButton:pressed  {\n"
"background-color:transparent;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}\n"
"\n"
"QToolButton:checked  {\n"
"background-color:transparent;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}\n"
"QListWidget {background-color:transparent;}\n"
"QScrollArea {background-color:transparent;}")
        self.gridLayout_2 = QGridLayout(BookInfo)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea = SmoothScrollArea(BookInfo)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 872, 699))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.picture = QLabel(self.scrollAreaWidgetContents)
        self.picture.setObjectName(u"picture")
        self.picture.setMinimumSize(QSize(300, 400))

        self.horizontalLayout.addWidget(self.picture)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(40, 16777215))
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.label)

        self.title = QLabel(self.scrollAreaWidgetContents)
        self.title.setObjectName(u"title")
        self.title.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.title)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_8.addWidget(self.label_6)

        self.idLabel = QLabel(self.scrollAreaWidgetContents)
        self.idLabel.setObjectName(u"idLabel")

        self.horizontalLayout_8.addWidget(self.idLabel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 0))
        self.label_2.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_11.addWidget(self.label_2)

        self.autorList = TagListWidget(self.scrollAreaWidgetContents)
        self.autorList.setObjectName(u"autorList")
        self.autorList.setMaximumSize(QSize(16777215, 60))
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
        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(40, 16777215))
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.description = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.description.setObjectName(u"description")
        self.description.setStyleSheet(u"QPlainTextEdit {background-color:transparent;}")
        self.description.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.description)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_6.addWidget(self.label_4)

        self.categoriesList = TagListWidget(self.scrollAreaWidgetContents)
        self.categoriesList.setObjectName(u"categoriesList")
        self.categoriesList.setMaximumSize(QSize(16777215, 60))
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
        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_7.addWidget(self.label_5)

        self.tagList = QWidget(self.scrollAreaWidgetContents)
        self.tagList.setObjectName(u"tagList")
        self.tagList.setStyleSheet(u"QPushButton {\n"
"    background-color:rgb(251, 239, 243);\n"
"    color: rgb(196, 95, 125);\n"
"	border:2px solid red;\n"
"    border-radius: 10px;\n"
"	border-color:rgb(196, 95, 125);\n"
"}\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QPushButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"")

        self.horizontalLayout_7.addWidget(self.tagList)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(55, 20))

        self.horizontalLayout_9.addWidget(self.label_7)

        self.views = QLabel(self.scrollAreaWidgetContents)
        self.views.setObjectName(u"views")
        self.views.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_9.addWidget(self.views)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.commandLinkButton = QCommandLinkButton(self.scrollAreaWidgetContents)
        self.commandLinkButton.setObjectName(u"commandLinkButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandLinkButton.sizePolicy().hasHeightForWidth())
        self.commandLinkButton.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.commandLinkButton)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.user_icon = HeadLabel(self.tab)
        self.user_icon.setObjectName(u"user_icon")
        self.user_icon.setMinimumSize(QSize(50, 50))
        self.user_icon.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_10.addWidget(self.user_icon)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.user_name = QLabel(self.tab)
        self.user_name.setObjectName(u"user_name")

        self.verticalLayout_5.addWidget(self.user_name)

        self.updateTick = QLabel(self.tab)
        self.updateTick.setObjectName(u"updateTick")

        self.verticalLayout_5.addWidget(self.updateTick)


        self.horizontalLayout_10.addLayout(self.verticalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.starButton = IconToolButton(self.tab)
        self.starButton.setObjectName(u"starButton")
        self.starButton.setMinimumSize(QSize(40, 40))
        self.starButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.starButton.setFocusPolicy(Qt.NoFocus)
        self.starButton.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/png/icon/icon_bookmark_off.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u":/png/icon/icon_bookmark_on.png", QSize(), QIcon.Selected, QIcon.On)
        self.starButton.setIcon(icon)
        self.starButton.setIconSize(QSize(50, 50))
        self.starButton.setCheckable(False)
        self.starButton.setChecked(False)
        self.starButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.starButton)

        self.favoriteButton = IconToolButton(self.tab)
        self.favoriteButton.setObjectName(u"favoriteButton")
        self.favoriteButton.setMinimumSize(QSize(40, 40))
        self.favoriteButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.favoriteButton.setStyleSheet(u"background-color:transparent;")
        icon1 = QIcon()
        icon1.addFile(u":/png/icon/icon_like_off.png", QSize(), QIcon.Normal, QIcon.Off)
        icon1.addFile(u":/png/icon/icon_bookmark_on.png", QSize(), QIcon.Selected, QIcon.On)
        self.favoriteButton.setIcon(icon1)
        self.favoriteButton.setIconSize(QSize(50, 50))
        self.favoriteButton.setCheckable(False)
        self.favoriteButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.favoriteButton)

        self.commentButton = IconToolButton(self.tab)
        self.commentButton.setObjectName(u"commentButton")
        self.commentButton.setMinimumSize(QSize(40, 40))
        self.commentButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.commentButton.setStyleSheet(u"background-color:transparent;")
        icon2 = QIcon()
        icon2.addFile(u":/png/icon/icon_comment.png", QSize(), QIcon.Normal, QIcon.Off)
        self.commentButton.setIcon(icon2)
        self.commentButton.setIconSize(QSize(50, 50))
        self.commentButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.commentButton)

        self.downloadButton = IconToolButton(self.tab)
        self.downloadButton.setObjectName(u"downloadButton")
        self.downloadButton.setMinimumSize(QSize(40, 40))
        self.downloadButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.downloadButton.setStyleSheet(u"background-color:transparent;")
        icon3 = QIcon()
        icon3.addFile(u":/png/icon/ic_get_app_black_36dp.png", QSize(), QIcon.Normal, QIcon.Off)
        self.downloadButton.setIcon(icon3)
        self.downloadButton.setIconSize(QSize(50, 50))
        self.downloadButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.downloadButton)

        self.uploadButton = QToolButton(self.tab)
        self.uploadButton.setObjectName(u"uploadButton")
        self.uploadButton.setMinimumSize(QSize(40, 40))
        icon4 = QIcon()
        icon4.addFile(u":/png/icon/upload.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.uploadButton.setIcon(icon4)
        self.uploadButton.setIconSize(QSize(50, 50))
        self.uploadButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.uploadButton)

        self.clearButton = QToolButton(self.tab)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setMinimumSize(QSize(40, 40))
        icon5 = QIcon()
        icon5.addFile(u":/png/icon/clear_off.png", QSize(), QIcon.Normal, QIcon.Off)
        self.clearButton.setIcon(icon5)
        self.clearButton.setIconSize(QSize(50, 50))
        self.clearButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.clearButton)

        self.startRead = QPushButton(self.tab)
        self.startRead.setObjectName(u"startRead")
        self.startRead.setMinimumSize(QSize(0, 40))
        self.startRead.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_2.addWidget(self.startRead)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pageLabel = QLabel(self.tab)
        self.pageLabel.setObjectName(u"pageLabel")

        self.horizontalLayout_2.addWidget(self.pageLabel)

        self.pageBox = QComboBox(self.tab)
        self.pageBox.setObjectName(u"pageBox")
        self.pageBox.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_2.addWidget(self.pageBox)


        self.horizontalLayout_10.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.epsListWidget = EpsListWidget(self.tab)
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

        self.verticalLayout.addWidget(self.epsListWidget)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_6 = QVBoxLayout(self.tab_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_8 = QLabel(self.tab_3)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_12.addWidget(self.label_8)

        self.readOffline = QPushButton(self.tab_3)
        self.readOffline.setObjectName(u"readOffline")
        self.readOffline.setMinimumSize(QSize(0, 40))
        self.readOffline.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_12.addWidget(self.readOffline)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_3)

        self.horizontalSpacer_4 = QSpacerItem(120, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_12)

        self.listWidget = EpsListWidget(self.tab_3)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
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
        self.listWidget.setSpacing(6)

        self.verticalLayout_6.addWidget(self.listWidget)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout_3.addWidget(self.tabWidget, 1, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(BookInfo)
        self.startRead.clicked.connect(BookInfo.StartRead)
        self.starButton.clicked.connect(BookInfo.AddBookLike)
        self.favoriteButton.clicked.connect(BookInfo.AddFavorite)
        self.downloadButton.clicked.connect(BookInfo.AddDownload)
        self.clearButton.clicked.connect(BookInfo.ClearCache)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(BookInfo)
    # setupUi

    def retranslateUi(self, BookInfo):
        BookInfo.setWindowTitle(QCoreApplication.translate("BookInfo", u"\u6f2b\u753b\u8be6\u60c5", None))
        self.picture.setText(QCoreApplication.translate("BookInfo", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("BookInfo", u"\u6807\u9898\uff1a", None))
        self.title.setText(QCoreApplication.translate("BookInfo", u"\u6807\u9898", None))
        self.label_6.setText(QCoreApplication.translate("BookInfo", u"id:", None))
        self.idLabel.setText("")
        self.label_2.setText(QCoreApplication.translate("BookInfo", u"\u4f5c\u8005\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("BookInfo", u"\u63cf\u8ff0\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("BookInfo", u"\u5206\u7c7b\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("BookInfo", u"Tags\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("BookInfo", u"\u89c2\u770b\u6570\uff1a", None))
        self.views.setText(QCoreApplication.translate("BookInfo", u"\u89c2\u770b\u6570", None))
        self.commandLinkButton.setText(QCoreApplication.translate("BookInfo", u"\u770b\u4e86\u8fd9\u8fb9\u672c\u5b50\u7684\u4eba\u4e5f\u5728\u770b", None))
        self.user_icon.setText(QCoreApplication.translate("BookInfo", u"TextLabel", None))
        self.user_name.setText(QCoreApplication.translate("BookInfo", u"TextLabel", None))
        self.updateTick.setText(QCoreApplication.translate("BookInfo", u"TextLabel", None))
        self.starButton.setText(QCoreApplication.translate("BookInfo", u"\u7231\u5fc3", None))
        self.favoriteButton.setText(QCoreApplication.translate("BookInfo", u"\u6536\u85cf", None))
        self.commentButton.setText(QCoreApplication.translate("BookInfo", u"\u8bc4\u8bba", None))
        self.downloadButton.setText(QCoreApplication.translate("BookInfo", u"\u4e0b\u8f7d", None))
        self.uploadButton.setText(QCoreApplication.translate("BookInfo", u"\u5b58\u50a8", None))
        self.clearButton.setText(QCoreApplication.translate("BookInfo", u"\u6e05\u7406", None))
        self.startRead.setText(QCoreApplication.translate("BookInfo", u"\u5f00\u59cb\u9605\u8bfb", None))
        self.pageLabel.setText(QCoreApplication.translate("BookInfo", u"\u5206\u9875\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("BookInfo", u"\u9605\u8bfb", None))
        self.label_8.setText(QCoreApplication.translate("BookInfo", u"\u53ef\u79bb\u7ebf\u9605\u8bfb\u5df2\u4e0b\u8f7d\u7684\u7ae0\u8282\uff1a", None))
        self.readOffline.setText(QCoreApplication.translate("BookInfo", u"\u5f00\u59cb\u9605\u8bfb", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("BookInfo", u"\u5df2\u4e0b\u8f7d\u7ae0\u8282", None))
    # retranslateUi

