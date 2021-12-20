# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_title_bar.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

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
        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.label_2 = QLabel(TitleBar)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(25, 25))
        self.label_2.setMaximumSize(QSize(25, 25))
        self.label_2.setStyleSheet(u"border-image: url(:/png/icon/logo_round.png);")
        self.label_2.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.horizontalLayout_2.addWidget(self.label_2, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.label = QLabel(TitleBar)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 40))
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.minButton = QToolButton(TitleBar)
        self.minButton.setObjectName(u"minButton")
        self.minButton.setMinimumSize(QSize(57, 40))
        self.minButton.setStyleSheet(u"QToolButton{ border-image:url(:/title_bar/open_black_min_button_57_40.png);}\n"
"QToolButton:hover{ border-image:url(:/title_bar/green_min_button_hover_57_40.png);}\n"
"QToolButton:pressed{ border-image:url(:/title_bar/black_min_button_pressed_57_40.png);}\n"
"border: none; margin: 0px")

        self.horizontalLayout_2.addWidget(self.minButton)

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

        self.horizontalLayout_2.addWidget(self.maxBt)

        self.closeButton = QToolButton(TitleBar)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(57, 40))
        self.closeButton.setStyleSheet(u"QToolButton{ border-image:url(:/title_bar/open_black_close_button_57_40.png);}\n"
"QToolButton:hover{ border-image:url(:/title_bar/close_button_hover_57_40.png);}\n"
"QToolButton:pressed{ border-image:url(:/title_bar/close_button_pressed_57_40.png);}\n"
"border: none; margin: 0px")

        self.horizontalLayout_2.addWidget(self.closeButton)


        self.retranslateUi(TitleBar)

        QMetaObject.connectSlotsByName(TitleBar)
    # setupUi

    def retranslateUi(self, TitleBar):
        TitleBar.setWindowTitle(QCoreApplication.translate("TitleBar", u"Form", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("TitleBar", u"PicACG", None))
        self.minButton.setText("")
        self.maxBt.setText("")
        self.closeButton.setText("")
    # retranslateUi

