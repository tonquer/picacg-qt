# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_navigation.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget)

from component.label.head_label import HeadLabel
from component.scroll_area.smooth_scroll_area import SmoothScrollArea
import images_rc

class Ui_Navigation(object):
    def setupUi(self, Navigation):
        if not Navigation.objectName():
            Navigation.setObjectName(u"Navigation")
        Navigation.resize(248, 473)
        Navigation.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(Navigation)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Navigation)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.picLabel = HeadLabel(self.widget)
        self.picLabel.setObjectName(u"picLabel")
        self.picLabel.setMinimumSize(QSize(100, 100))
        self.picLabel.setMaximumSize(QSize(100, 100))
        self.picLabel.setPixmap(QPixmap(u":/png/icon/placeholder_avatar.png"))
        self.picLabel.setScaledContents(True)

        self.verticalLayout.addWidget(self.picLabel, 0, Qt.AlignHCenter)

        self.nameLabel = QLabel(self.widget)
        self.nameLabel.setObjectName(u"nameLabel")

        self.verticalLayout.addWidget(self.nameLabel)

        self.titleLabel = QLabel(self.widget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.expLabel = QLabel(self.widget)
        self.expLabel.setObjectName(u"expLabel")

        self.horizontalLayout.addWidget(self.expLabel)

        self.levelLabel = QLabel(self.widget)
        self.levelLabel.setObjectName(u"levelLabel")

        self.horizontalLayout.addWidget(self.levelLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.scrollArea = SmoothScrollArea(self.widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 230, 602))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 9, 0, 9)
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.collectButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup = QButtonGroup(Navigation)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.collectButton)
        self.collectButton.setObjectName(u"collectButton")
        self.collectButton.setMinimumSize(QSize(230, 40))
        icon = QIcon()
        icon.addFile(u":/images/menu/Contact.png", QSize(), QIcon.Normal, QIcon.Off)
        self.collectButton.setIcon(icon)
        self.collectButton.setIconSize(QSize(32, 32))
        self.collectButton.setCheckable(True)
        self.collectButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.collectButton)

        self.myCommentButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.myCommentButton)
        self.myCommentButton.setObjectName(u"myCommentButton")
        self.myCommentButton.setMinimumSize(QSize(230, 40))
        self.myCommentButton.setIcon(icon)
        self.myCommentButton.setIconSize(QSize(32, 32))
        self.myCommentButton.setCheckable(True)
        self.myCommentButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.myCommentButton)

        self.lookButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.lookButton)
        self.lookButton.setObjectName(u"lookButton")
        self.lookButton.setMinimumSize(QSize(230, 40))
        self.lookButton.setIcon(icon)
        self.lookButton.setIconSize(QSize(32, 32))
        self.lookButton.setCheckable(True)
        self.lookButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.lookButton)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.indexButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.indexButton)
        self.indexButton.setObjectName(u"indexButton")
        self.indexButton.setMinimumSize(QSize(230, 40))
        self.indexButton.setIcon(icon)
        self.indexButton.setIconSize(QSize(32, 32))
        self.indexButton.setCheckable(True)
        self.indexButton.setChecked(True)
        self.indexButton.setPopupMode(QToolButton.DelayedPopup)
        self.indexButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.indexButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_3.addWidget(self.indexButton)

        self.searchButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.searchButton)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setMinimumSize(QSize(230, 40))
        self.searchButton.setIcon(icon)
        self.searchButton.setIconSize(QSize(32, 32))
        self.searchButton.setCheckable(True)
        self.searchButton.setPopupMode(QToolButton.DelayedPopup)
        self.searchButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.searchButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_3.addWidget(self.searchButton)

        self.msgButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.msgButton)
        self.msgButton.setObjectName(u"msgButton")
        self.msgButton.setMinimumSize(QSize(230, 40))
        self.msgButton.setIcon(icon)
        self.msgButton.setIconSize(QSize(32, 32))
        self.msgButton.setCheckable(True)
        self.msgButton.setPopupMode(QToolButton.DelayedPopup)
        self.msgButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.msgButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_3.addWidget(self.msgButton)

        self.categoryButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.categoryButton)
        self.categoryButton.setObjectName(u"categoryButton")
        self.categoryButton.setMinimumSize(QSize(230, 40))
        self.categoryButton.setIcon(icon)
        self.categoryButton.setIconSize(QSize(32, 32))
        self.categoryButton.setCheckable(True)
        self.categoryButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.categoryButton)

        self.rankButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.rankButton)
        self.rankButton.setObjectName(u"rankButton")
        self.rankButton.setMinimumSize(QSize(230, 40))
        self.rankButton.setIcon(icon)
        self.rankButton.setIconSize(QSize(32, 32))
        self.rankButton.setCheckable(True)
        self.rankButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.rankButton)

        self.chatButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.chatButton)
        self.chatButton.setObjectName(u"chatButton")
        self.chatButton.setMinimumSize(QSize(230, 40))
        self.chatButton.setIcon(icon)
        self.chatButton.setIconSize(QSize(32, 32))
        self.chatButton.setCheckable(True)
        self.chatButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.chatButton)

        self.gameButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.gameButton)
        self.gameButton.setObjectName(u"gameButton")
        self.gameButton.setMinimumSize(QSize(230, 40))
        self.gameButton.setIcon(icon)
        self.gameButton.setIconSize(QSize(32, 32))
        self.gameButton.setCheckable(True)
        self.gameButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.gameButton)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.downloadButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.downloadButton)
        self.downloadButton.setObjectName(u"downloadButton")
        self.downloadButton.setMinimumSize(QSize(230, 40))
        self.downloadButton.setIcon(icon)
        self.downloadButton.setIconSize(QSize(32, 32))
        self.downloadButton.setCheckable(True)
        self.downloadButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.downloadButton)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.line_3 = QFrame(self.widget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.helpButton = QToolButton(self.widget)
        self.buttonGroup.addButton(self.helpButton)
        self.helpButton.setObjectName(u"helpButton")
        self.helpButton.setMinimumSize(QSize(230, 40))
        self.helpButton.setIcon(icon)
        self.helpButton.setIconSize(QSize(32, 32))
        self.helpButton.setCheckable(True)
        self.helpButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout.addWidget(self.helpButton)

        self.settingButton = QToolButton(self.widget)
        self.buttonGroup.addButton(self.settingButton)
        self.settingButton.setObjectName(u"settingButton")
        self.settingButton.setMinimumSize(QSize(230, 40))
        self.settingButton.setStyleSheet(u"")
        self.settingButton.setIcon(icon)
        self.settingButton.setIconSize(QSize(32, 32))
        self.settingButton.setCheckable(True)
        self.settingButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.settingButton.setAutoRaise(False)

        self.verticalLayout.addWidget(self.settingButton)


        self.verticalLayout_2.addWidget(self.widget)


        self.retranslateUi(Navigation)

        QMetaObject.connectSlotsByName(Navigation)
    # setupUi

    def retranslateUi(self, Navigation):
        Navigation.setWindowTitle(QCoreApplication.translate("Navigation", u"\u5bfc\u822a", None))
        self.picLabel.setText("")
        self.nameLabel.setText("")
        self.titleLabel.setText("")
        self.expLabel.setText("")
        self.levelLabel.setText("")
        self.pushButton.setText(QCoreApplication.translate("Navigation", u"\u767b\u5f55", None))
        self.label.setText(QCoreApplication.translate("Navigation", u"\u7528\u6237", None))
        self.collectButton.setText(QCoreApplication.translate("Navigation", u"\u6211\u7684\u6536\u85cf", None))
        self.myCommentButton.setText(QCoreApplication.translate("Navigation", u"\u6211\u7684\u8bc4\u8bba", None))
        self.lookButton.setText(QCoreApplication.translate("Navigation", u"\u89c2\u770b\u8bb0\u5f55", None))
        self.label_2.setText(QCoreApplication.translate("Navigation", u"\u5bfc\u822a", None))
        self.indexButton.setText(QCoreApplication.translate("Navigation", u"\u9996\u9875", None))
        self.searchButton.setText(QCoreApplication.translate("Navigation", u"\u641c\u7d22", None))
        self.msgButton.setText(QCoreApplication.translate("Navigation", u"\u7559\u8a00\u677f", None))
        self.categoryButton.setText(QCoreApplication.translate("Navigation", u"\u5206\u7c7b", None))
        self.rankButton.setText(QCoreApplication.translate("Navigation", u"\u6392\u884c\u699c", None))
        self.chatButton.setText(QCoreApplication.translate("Navigation", u"\u804a\u5929\u5ba4", None))
        self.gameButton.setText(QCoreApplication.translate("Navigation", u"\u6e38\u620f\u533a", None))
        self.label_3.setText(QCoreApplication.translate("Navigation", u"\u5176\u4ed6", None))
        self.downloadButton.setText(QCoreApplication.translate("Navigation", u"\u4e0b\u8f7d", None))
        self.helpButton.setText(QCoreApplication.translate("Navigation", u"\u5e2e\u52a9", None))
        self.settingButton.setText(QCoreApplication.translate("Navigation", u"\u8bbe\u7f6e", None))
    # retranslateUi

