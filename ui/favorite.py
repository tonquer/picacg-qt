# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'favorite.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_favorite(object):
    def setupUi(self, favorite):
        if not favorite.objectName():
            favorite.setObjectName(u"favorite")
        favorite.resize(451, 292)
        self.gridLayout_2 = QGridLayout(favorite)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.nums = QLabel(favorite)
        self.nums.setObjectName(u"nums")

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(favorite)
        self.pages.setObjectName(u"pages")

        self.horizontalLayout.addWidget(self.pages)

        self.comboBox = QComboBox(favorite)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(75, 0))

        self.horizontalLayout.addWidget(self.comboBox)

        self.lineEdit = QLineEdit(favorite)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.jumpButton = QPushButton(favorite)
        self.jumpButton.setObjectName(u"jumpButton")

        self.horizontalLayout.addWidget(self.jumpButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 1, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")

        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.retranslateUi(favorite)
        self.jumpButton.clicked.connect(favorite.JumpPage)
        self.comboBox.currentIndexChanged.connect(favorite.RefreshDataFocus)

        QMetaObject.connectSlotsByName(favorite)
    # setupUi

    def retranslateUi(self, favorite):
        favorite.setWindowTitle(QCoreApplication.translate("favorite", u"Form", None))
        self.nums.setText(QCoreApplication.translate("favorite", u"\u6536\u85cf\u6570\uff1a", None))
        self.pages.setText(QCoreApplication.translate("favorite", u"\u9875", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("favorite", u"\u4ece\u65b0\u5230\u65e7", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("favorite", u"\u4ece\u65e7\u5230\u65b0", None))

        self.jumpButton.setText(QCoreApplication.translate("favorite", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("favorite", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

