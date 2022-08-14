# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_title_bar.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QToolButton, QWidget)
import images_rc

class Ui_TitleBar(object):
    def setupUi(self, TitleBar):
        if not TitleBar.objectName():
            TitleBar.setObjectName(u"TitleBar")
        TitleBar.resize(1360, 49)
        TitleBar.setStyleSheet(u"")
        self.horizontalLayout_2 = QHBoxLayout(TitleBar)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(8, -1, -1, -1)
        self.label_2 = QLabel(TitleBar)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(25, 25))
        self.label_2.setMaximumSize(QSize(25, 25))
        self.label_2.setStyleSheet(u"border-image: url(:/png/icon/logo_round.png);")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label = QLabel(TitleBar)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 40))
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)

        self.subTitle = QLabel(TitleBar)
        self.subTitle.setObjectName(u"subTitle")
        self.subTitle.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.subTitle)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.minButton = QToolButton(TitleBar)
        self.minButton.setObjectName(u"minButton")
        self.minButton.setMinimumSize(QSize(57, 40))
        self.minButton.setStyleSheet(u"QToolButton{ border-image:url(:/title_bar/open_black_min_button_57_40.png);}\n"
"QToolButton:hover{ border-image:url(:/title_bar/green_min_button_hover_57_40.png);}\n"
"QToolButton:pressed{ border-image:url(:/title_bar/black_min_button_pressed_57_40.png);}\n"
"border: none; margin: 0px")

        self.horizontalLayout_4.addWidget(self.minButton)

        self.maxBt = QToolButton(TitleBar)
        self.maxBt.setObjectName(u"maxBt")
        self.maxBt.setMinimumSize(QSize(57, 40))
        self.maxBt.setStyleSheet(u"QToolButton[isMax=false]{ border-image:url(:/title_bar/open_black_max_button_57_40.png);}\n"
"QToolButton:hover[isMax=false]{ border-image:url(:/title_bar/green_max_button_hover_57_40.png);}\n"
"QToolButton:pressed[isMax=false]{ border-image:url(:/title_bar/black_max_button_pressed_57_40.png);}\n"
"QToolButton[isMax=true]{ border-image:url(:/title_bar/black_down_button_57_40.png);}\n"
"QToolButton:hover[isMax=true]{ border-image:url(:/title_bar/green_down_button_hover_57_40.png);}\n"
"QToolButton:pressed[isMax=true]{ border-image:url(:/title_bar/down_button_pressed_57_40.png);}\n"
"border: none;\n"
"margin: 0px")
        self.maxBt.setProperty("isMax", False)

        self.horizontalLayout_4.addWidget(self.maxBt)

        self.closeButton = QToolButton(TitleBar)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(57, 40))
        self.closeButton.setStyleSheet(u"QToolButton{ border-image:url(:/title_bar/open_black_close_button_57_40.png);}\n"
"QToolButton:hover{ border-image:url(:/title_bar/close_button_hover_57_40.png);}\n"
"QToolButton:pressed{ border-image:url(:/title_bar/close_button_pressed_57_40.png);}\n"
"border: none; margin: 0px")

        self.horizontalLayout_4.addWidget(self.closeButton)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)

        self.retranslateUi(TitleBar)

        QMetaObject.connectSlotsByName(TitleBar)
    # setupUi

    def retranslateUi(self, TitleBar):
        TitleBar.setWindowTitle(QCoreApplication.translate("TitleBar", u"Form", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("TitleBar", u"PicACG", None))
        self.subTitle.setText("")
        self.minButton.setText("")
        self.maxBt.setText("")
        self.closeButton.setText("")
    # retranslateUi

