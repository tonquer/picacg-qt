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

from .qtlistwidget import QtBookList
from .qtlistwidget import QtCategoryList
from .completelineedit import CompleteLineEdit


class Ui_search(object):
    def setupUi(self, search):
        if not search.objectName():
            search.setObjectName(u"search")
        search.resize(827, 585)
        self.gridLayout_2 = QGridLayout(search)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.localBox = QRadioButton(search)
        self.localBox.setObjectName(u"localBox")
        self.localBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.localBox)

        self.titleBox = QCheckBox(search)
        self.titleBox.setObjectName(u"titleBox")
        self.titleBox.setEnabled(True)
        self.titleBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.titleBox)

        self.desBox = QCheckBox(search)
        self.desBox.setObjectName(u"desBox")
        self.desBox.setEnabled(True)
        self.desBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.desBox)

        self.authorBox = QCheckBox(search)
        self.authorBox.setObjectName(u"authorBox")
        self.authorBox.setEnabled(True)
        self.authorBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.authorBox)

        self.tagsBox = QCheckBox(search)
        self.tagsBox.setObjectName(u"tagsBox")
        self.tagsBox.setEnabled(True)
        self.tagsBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.tagsBox)

        self.categoryBox = QCheckBox(search)
        self.categoryBox.setObjectName(u"categoryBox")
        self.categoryBox.setEnabled(True)
        self.categoryBox.setChecked(True)

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

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.searchEdit = CompleteLineEdit(search)
        self.searchEdit.setObjectName(u"searchEdit")
        self.searchEdit.setMinimumSize(QSize(0, 30))
        self.searchEdit.setMaximumSize(QSize(16777215, 30))
        self.searchEdit.setStyleSheet(u"QLineEdit {background-color:transparent;}")

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

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.line_4 = QFrame(search)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.label = QLabel(search)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 30))
        self.label.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.label)

        self.line_5 = QFrame(search)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_5)

        self.spinBox = QSpinBox(search)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 0))
        self.spinBox.setStyleSheet(u"background-color:transparent;")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_6 = QFrame(search)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_6)

        self.jumpPage = QPushButton(search)
        self.jumpPage.setObjectName(u"jumpPage")
        self.jumpPage.setMinimumSize(QSize(60, 30))
        self.jumpPage.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.jumpPage)


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.bookLayout = QGridLayout()
        self.bookLayout.setObjectName(u"bookLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(search)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 0))
        self.label_4.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_3.addWidget(self.label_4)

        self.categoryList = QtCategoryList(search)
        self.categoryList.setObjectName(u"categoryList")
        self.categoryList.setMaximumSize(QSize(16777215, 40))
        self.categoryList.setStyleSheet(u"QListWidget {background-color:transparent;}")
        self.categoryList.setFrameShape(QFrame.StyledPanel)
        self.categoryList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.categoryList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.categoryList.setFlow(QListView.LeftToRight)
        self.categoryList.setSpacing(6)

        self.horizontalLayout_3.addWidget(self.categoryList)


        self.bookLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.bookList = QtBookList(search)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.bookLayout.addWidget(self.bookList, 0, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(search)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(80, 0))
        self.label_5.setMaximumSize(QSize(80, 50))

        self.horizontalLayout_4.addWidget(self.label_5)

        self.keywordList = QtCategoryList(search)
        self.keywordList.setObjectName(u"keywordList")
        self.keywordList.setMinimumSize(QSize(0, 0))
        self.keywordList.setMaximumSize(QSize(16777215, 50))
        self.keywordList.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
"QListWidget::item {\n"
"    background-color:rgb(251, 239, 243);\n"
"    color: rgb(196, 95, 125);\n"
"	border:2px solid red;\n"
"	border-color:rgb(196, 95, 125);\n"
"	border-radius: 15px;\n"
"}\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QListWidget::item:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 15px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"")
        self.keywordList.setFrameShape(QFrame.NoFrame)
        self.keywordList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.keywordList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.keywordList.setFlow(QListView.LeftToRight)
        self.keywordList.setSpacing(6)

        self.horizontalLayout_4.addWidget(self.keywordList)


        self.bookLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)


        self.gridLayout_2.addLayout(self.bookLayout, 0, 0, 1, 1)


        self.retranslateUi(search)
        self.searchButton.clicked.connect(search.Search)
        self.jumpPage.clicked.connect(search.JumpPage)
        self.comboBox.currentIndexChanged.connect(search.ChangeSort)
        self.localBox.clicked.connect(search.SetSearch)
        self.sortKey.currentIndexChanged.connect(search.ChangeSort)
        self.sortId.currentIndexChanged.connect(search.ChangeSort)

        QMetaObject.connectSlotsByName(search)
    # setupUi

    def retranslateUi(self, search):
        search.setWindowTitle(QCoreApplication.translate("search", u"Form", None))
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
        self.label_4.setText(QCoreApplication.translate("search", u"\u5c4f\u853d\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("search", u"\u5927\u5bb6\u90fd\u5728\u641c\uff1a", None))
    # retranslateUi

