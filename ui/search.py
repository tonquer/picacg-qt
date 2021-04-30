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

from .completelineedit import CompleteLineEdit


class Ui_search(object):
    def setupUi(self, search):
        if not search.objectName():
            search.setObjectName(u"search")
        search.resize(613, 585)
        self.gridLayout_2 = QGridLayout(search)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.searchEdit = CompleteLineEdit(search)
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


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.bookLayout = QGridLayout()
        self.bookLayout.setObjectName(u"bookLayout")

        self.gridLayout_2.addLayout(self.bookLayout, 0, 0, 1, 1)

        self.comboBoxLayout = QVBoxLayout()
        self.comboBoxLayout.setObjectName(u"comboBoxLayout")
        self.groupBox = QGroupBox(search)
        self.groupBox.setObjectName(u"groupBox")

        self.comboBoxLayout.addWidget(self.groupBox)


        self.gridLayout_2.addLayout(self.comboBoxLayout, 3, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.localBox = QRadioButton(search)
        self.localBox.setObjectName(u"localBox")

        self.horizontalLayout_2.addWidget(self.localBox)

        self.titleBox = QCheckBox(search)
        self.titleBox.setObjectName(u"titleBox")
        self.titleBox.setEnabled(False)
        self.titleBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.titleBox)

        self.desBox = QCheckBox(search)
        self.desBox.setObjectName(u"desBox")
        self.desBox.setEnabled(False)
        self.desBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.desBox)

        self.authorBox = QCheckBox(search)
        self.authorBox.setObjectName(u"authorBox")
        self.authorBox.setEnabled(False)
        self.authorBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.authorBox)

        self.tagsBox = QCheckBox(search)
        self.tagsBox.setObjectName(u"tagsBox")
        self.tagsBox.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.tagsBox)

        self.categoryBox = QCheckBox(search)
        self.categoryBox.setObjectName(u"categoryBox")
        self.categoryBox.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.categoryBox)

        self.sortKey = QComboBox(search)
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.setObjectName(u"sortKey")
        self.sortKey.setEnabled(False)
        self.sortKey.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.sortKey)

        self.sortId = QComboBox(search)
        self.sortId.addItem("")
        self.sortId.addItem("")
        self.sortId.setObjectName(u"sortId")
        self.sortId.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.sortId)

        self.line = QFrame(search)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line)

        self.label_3 = QLabel(search)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.numsLabel = QLabel(search)
        self.numsLabel.setObjectName(u"numsLabel")

        self.horizontalLayout_2.addWidget(self.numsLabel)

        self.line_2 = QFrame(search)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line_2)

        self.label_2 = QLabel(search)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.timesLabel = QLabel(search)
        self.timesLabel.setObjectName(u"timesLabel")

        self.horizontalLayout_2.addWidget(self.timesLabel)

        self.line_3 = QFrame(search)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)


        self.retranslateUi(search)
        self.searchButton.clicked.connect(search.Search)
        self.jumpPage.clicked.connect(search.JumpPage)
        self.comboBox.currentIndexChanged.connect(search.ChangeSort)
        self.localBox.clicked.connect(search.SetSearch)

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
        self.localBox.setText(QCoreApplication.translate("search", u"\u4f7f\u7528\u672c\u5730\u641c\u7d22", None))
        self.titleBox.setText(QCoreApplication.translate("search", u"\u6807\u9898", None))
        self.desBox.setText(QCoreApplication.translate("search", u"\u5185\u5bb9", None))
        self.authorBox.setText(QCoreApplication.translate("search", u"\u4f5c\u8005", None))
        self.tagsBox.setText(QCoreApplication.translate("search", u"tags", None))
        self.categoryBox.setText(QCoreApplication.translate("search", u"\u5206\u7c7b", None))
        self.sortKey.setItemText(0, QCoreApplication.translate("search", u"\u66f4\u65b0\u65f6\u95f4", None))
        self.sortKey.setItemText(1, QCoreApplication.translate("search", u"\u521b\u5efa\u65f6\u95f4", None))
        self.sortKey.setItemText(2, QCoreApplication.translate("search", u"\u7231\u5fc3\u6570", None))
        self.sortKey.setItemText(3, QCoreApplication.translate("search", u"\u89c2\u770b\u6570", None))
        self.sortKey.setItemText(4, QCoreApplication.translate("search", u"\u7ae0\u8282\u6570", None))
        self.sortKey.setItemText(5, QCoreApplication.translate("search", u"\u56fe\u7247\u6570", None))

        self.sortId.setItemText(0, QCoreApplication.translate("search", u"\u964d\u5e8f", None))
        self.sortId.setItemText(1, QCoreApplication.translate("search", u"\u5347\u5e8f", None))

        self.label_3.setText(QCoreApplication.translate("search", u"\u672c\u5730\u6570\u91cf\uff1a", None))
        self.numsLabel.setText(QCoreApplication.translate("search", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("search", u"\u66f4\u65b0\u65f6\u95f4\uff1a", None))
        self.timesLabel.setText(QCoreApplication.translate("search", u"TextLabel", None))
    # retranslateUi

