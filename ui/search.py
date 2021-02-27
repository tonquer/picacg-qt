# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_search(object):
    def setupUi(self, search):
        if not search.objectName():
            search.setObjectName(u"search")
        search.resize(613, 585)
        self.gridLayout_2 = QGridLayout(search)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.searchEdit = QLineEdit(search)
        self.searchEdit.setObjectName(u"searchEdit")
        self.searchEdit.setMinimumSize(QSize(0, 30))
        self.searchEdit.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.searchEdit)

        self.comboBox = QComboBox(search)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)

        self.searchButton = QPushButton(search)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setMinimumSize(QSize(0, 30))
        self.searchButton.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.searchButton)

        self.label = QLabel(search)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.label)

        self.jumpLine = QLineEdit(search)
        self.jumpLine.setObjectName(u"jumpLine")

        self.horizontalLayout.addWidget(self.jumpLine)

        self.jumpPage = QPushButton(search)
        self.jumpPage.setObjectName(u"jumpPage")
        self.jumpPage.setMinimumSize(QSize(0, 30))
        self.jumpPage.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.jumpPage)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.bookLayout = QGridLayout()
        self.bookLayout.setObjectName(u"bookLayout")

        self.gridLayout_2.addLayout(self.bookLayout, 0, 0, 1, 1)

        self.comboBoxLayout = QVBoxLayout()
        self.comboBoxLayout.setObjectName(u"comboBoxLayout")
        self.groupBox = QGroupBox(search)
        self.groupBox.setObjectName(u"groupBox")

        self.comboBoxLayout.addWidget(self.groupBox)


        self.gridLayout_2.addLayout(self.comboBoxLayout, 2, 0, 1, 1)


        self.retranslateUi(search)
        self.searchButton.clicked.connect(search.Search)
        self.jumpPage.clicked.connect(search.JumpPage)
        self.comboBox.currentIndexChanged.connect(search.ChangeSort)

        QMetaObject.connectSlotsByName(search)
    # setupUi

    def retranslateUi(self, search):
        search.setWindowTitle(QCoreApplication.translate("search", u"Form", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("search", u"\u65b0\u5230\u65e7", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("search", u"\u65e7\u5230\u65b0", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("search", u"\u6700\u591a\u7231\u5fc3", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("search", u"\u6700\u591a\u7ec5\u58eb\u6307\u6570", None))

        self.searchButton.setText(QCoreApplication.translate("search", u"\u641c\u7d22", None))
#if QT_CONFIG(shortcut)
        self.searchButton.setShortcut(QCoreApplication.translate("search", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("search", u"\u9875\uff1a0/0", None))
        self.jumpPage.setText(QCoreApplication.translate("search", u"\u8df3\u8f6c", None))
        self.groupBox.setTitle(QCoreApplication.translate("search", u"GroupBox", None))
    # retranslateUi

