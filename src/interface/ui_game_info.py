# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_game_info.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHBoxLayout,
    QLabel, QListWidgetItem, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)

from component.list.base_list_widget import BaseListWidget
import images_rc

class Ui_GameInfo(object):
    def setupUi(self, GameInfo):
        if not GameInfo.objectName():
            GameInfo.setObjectName(u"GameInfo")
        GameInfo.resize(900, 963)
        self.gridLayout_2 = QGridLayout(GameInfo)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.picture = QLabel(GameInfo)
        self.picture.setObjectName(u"picture")
        self.picture.setMinimumSize(QSize(320, 320))

        self.horizontalLayout.addWidget(self.picture)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(GameInfo)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(40, 16777215))
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.label)

        self.title = QLabel(GameInfo)
        self.title.setObjectName(u"title")
        self.title.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.title)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.icon_1 = QLabel(GameInfo)
        self.icon_1.setObjectName(u"icon_1")
        self.icon_1.setEnabled(True)
        self.icon_1.setMaximumSize(QSize(60, 60))
        self.icon_1.setPixmap(QPixmap(u":/png/icon/icon_game_recommend.png"))
        self.icon_1.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.icon_1)

        self.icon_2 = QLabel(GameInfo)
        self.icon_2.setObjectName(u"icon_2")
        self.icon_2.setMinimumSize(QSize(60, 60))
        self.icon_2.setMaximumSize(QSize(60, 60))
        self.icon_2.setPixmap(QPixmap(u":/png/icon/icon_adult.png"))
        self.icon_2.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.icon_2)

        self.icon_3 = QLabel(GameInfo)
        self.icon_3.setObjectName(u"icon_3")
        self.icon_3.setMinimumSize(QSize(60, 60))
        self.icon_3.setMaximumSize(QSize(60, 60))
        self.icon_3.setPixmap(QPixmap(u":/png/icon/icon_game_android.png"))
        self.icon_3.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.icon_3)

        self.icon_4 = QLabel(GameInfo)
        self.icon_4.setObjectName(u"icon_4")
        self.icon_4.setMinimumSize(QSize(60, 60))
        self.icon_4.setMaximumSize(QSize(60, 60))
        self.icon_4.setPixmap(QPixmap(u":/png/icon/icon_game_ios.png"))
        self.icon_4.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.icon_4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(GameInfo)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(40, 16777215))
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.description = QPlainTextEdit(GameInfo)
        self.description.setObjectName(u"description")
        self.description.setStyleSheet(u"QPlainTextEdit {background-color:transparent;}")

        self.horizontalLayout_5.addWidget(self.description)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.updateTick = QLabel(GameInfo)
        self.updateTick.setObjectName(u"updateTick")
        self.updateTick.setEnabled(True)
        self.updateTick.setMinimumSize(QSize(80, 40))
        self.updateTick.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_2.addWidget(self.updateTick)

        self.commentButton = QToolButton(GameInfo)
        self.commentButton.setObjectName(u"commentButton")
        self.commentButton.setMinimumSize(QSize(40, 40))
        self.commentButton.setStyleSheet(u"QToolButton\n"
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
"}")
        icon = QIcon()
        icon.addFile(u":/png/icon/icon_comment.png", QSize(), QIcon.Normal, QIcon.Off)
        self.commentButton.setIcon(icon)
        self.commentButton.setIconSize(QSize(50, 50))

        self.horizontalLayout_2.addWidget(self.commentButton)

        self.androidButton = QPushButton(GameInfo)
        self.androidButton.setObjectName(u"androidButton")
        self.androidButton.setMinimumSize(QSize(0, 40))
        self.androidButton.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_2.addWidget(self.androidButton)

        self.iosButton = QPushButton(GameInfo)
        self.iosButton.setObjectName(u"iosButton")
        self.iosButton.setMinimumSize(QSize(0, 40))
        self.iosButton.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_2.addWidget(self.iosButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.epsListWidget = BaseListWidget(GameInfo)
        self.epsListWidget.setObjectName(u"epsListWidget")
        self.epsListWidget.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
"")
        self.epsListWidget.setTextElideMode(Qt.ElideRight)
        self.epsListWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.epsListWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.epsListWidget.setSpacing(6)

        self.verticalLayout.addWidget(self.epsListWidget)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(GameInfo)
        self.iosButton.clicked.connect(GameInfo.CopyIos)
        self.androidButton.clicked.connect(GameInfo.CopyAndroid)

        QMetaObject.connectSlotsByName(GameInfo)
    # setupUi

    def retranslateUi(self, GameInfo):
        GameInfo.setWindowTitle(QCoreApplication.translate("GameInfo", u"\u6e38\u620f\u8be6\u60c5", None))
        self.picture.setText(QCoreApplication.translate("GameInfo", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("GameInfo", u"\u6807\u9898\uff1a", None))
        self.title.setText(QCoreApplication.translate("GameInfo", u"\u6807\u9898", None))
        self.icon_1.setText("")
        self.icon_2.setText("")
        self.icon_3.setText("")
        self.icon_4.setText("")
        self.label_3.setText(QCoreApplication.translate("GameInfo", u"\u63cf\u8ff0\uff1a", None))
        self.updateTick.setText(QCoreApplication.translate("GameInfo", u"TextLabel", None))
        self.commentButton.setText("")
        self.androidButton.setText(QCoreApplication.translate("GameInfo", u"\u590d\u5236\u5b89\u5353\u4e0b\u8f7d\u5730\u5740", None))
        self.iosButton.setText(QCoreApplication.translate("GameInfo", u"\u590d\u5236IOS\u4e0b\u8f7d\u5730\u5740", None))
    # retranslateUi

