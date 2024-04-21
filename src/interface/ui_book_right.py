# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_book_right.ui'
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
from PySide6.QtWidgets import (QApplication, QCommandLinkButton, QFrame, QHBoxLayout,
    QLabel, QLayout, QListView, QListWidgetItem,
    QPlainTextEdit, QSizePolicy, QVBoxLayout, QWidget)

from component.list.tag_list_widget import TagListWidget

class Ui_BookRight(object):
    def setupUi(self, BookRight):
        if not BookRight.objectName():
            BookRight.setObjectName(u"BookRight")
        BookRight.resize(400, 370)
        self.verticalLayout = QVBoxLayout(BookRight)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(BookRight)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(40, 16777215))
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.label)

        self.title = QLabel(BookRight)
        self.title.setObjectName(u"title")
        self.title.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.title)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_6 = QLabel(BookRight)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_8.addWidget(self.label_6)

        self.idLabel = QLabel(BookRight)
        self.idLabel.setObjectName(u"idLabel")

        self.horizontalLayout_8.addWidget(self.idLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_2 = QLabel(BookRight)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 0))
        self.label_2.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_11.addWidget(self.label_2)

        self.autorList = TagListWidget(BookRight)
        self.autorList.setObjectName(u"autorList")
        self.autorList.setMaximumSize(QSize(16777215, 60))
        self.autorList.setStyleSheet(u"background-color:transparent;")
        self.autorList.setFrameShape(QFrame.NoFrame)
        self.autorList.setProperty("showDropIndicator", True)
        self.autorList.setFlow(QListView.LeftToRight)
        self.autorList.setSpacing(10)

        self.horizontalLayout_11.addWidget(self.autorList)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(BookRight)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(40, 16777215))
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.description = QPlainTextEdit(BookRight)
        self.description.setObjectName(u"description")
        self.description.setStyleSheet(u"QPlainTextEdit {background-color:transparent;}")
        self.description.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.description)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(BookRight)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_6.addWidget(self.label_4)

        self.categoriesList = TagListWidget(BookRight)
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


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(BookRight)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_7.addWidget(self.label_5)

        self.tagList = QWidget(BookRight)
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


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_7 = QLabel(BookRight)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(55, 20))

        self.horizontalLayout_9.addWidget(self.label_7)

        self.views = QLabel(BookRight)
        self.views.setObjectName(u"views")
        self.views.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_9.addWidget(self.views)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.commandLinkButton = QCommandLinkButton(BookRight)
        self.commandLinkButton.setObjectName(u"commandLinkButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandLinkButton.sizePolicy().hasHeightForWidth())
        self.commandLinkButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.commandLinkButton)


        self.retranslateUi(BookRight)

        QMetaObject.connectSlotsByName(BookRight)
    # setupUi

    def retranslateUi(self, BookRight):
        BookRight.setWindowTitle(QCoreApplication.translate("BookRight", u"Form", None))
        self.label.setText(QCoreApplication.translate("BookRight", u"\u6807\u9898\uff1a", None))
        self.title.setText(QCoreApplication.translate("BookRight", u"\u6807\u9898", None))
        self.label_6.setText(QCoreApplication.translate("BookRight", u"id:", None))
        self.idLabel.setText("")
        self.label_2.setText(QCoreApplication.translate("BookRight", u"\u4f5c\u8005\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("BookRight", u"\u63cf\u8ff0\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("BookRight", u"\u5206\u7c7b\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("BookRight", u"Tags\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("BookRight", u"\u89c2\u770b\u6570\uff1a", None))
        self.views.setText(QCoreApplication.translate("BookRight", u"\u89c2\u770b\u6570", None))
        self.commandLinkButton.setText(QCoreApplication.translate("BookRight", u"\u770b\u4e86\u8fd9\u8fb9\u672c\u5b50\u7684\u4eba\u4e5f\u5728\u770b", None))
    # retranslateUi

