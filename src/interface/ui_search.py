# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_search.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QListView, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

from component.line_edit.search_line_edit import SearchLineEdit
from component.list.comic_list_widget import ComicListWidget
from component.list.tag_list_widget import TagListWidget

class Ui_Search(object):
    def setupUi(self, Search):
        if not Search.objectName():
            Search.setObjectName(u"Search")
        Search.resize(740, 369)
        Search.setMinimumSize(QSize(80, 0))
        self.verticalLayout = QVBoxLayout(Search)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Search)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(80, 0))
        self.label_2.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit = SearchLineEdit(Search)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(40, 40))
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.searchButton = QPushButton(Search)
        self.searchButton.setObjectName(u"searchButton")

        self.horizontalLayout_2.addWidget(self.searchButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(Search)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 0))
        self.label_4.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_3.addWidget(self.label_4)

        self.categoryList = TagListWidget(Search)
        self.categoryList.setObjectName(u"categoryList")
        self.categoryList.setMaximumSize(QSize(16777215, 40))
        self.categoryList.setStyleSheet(u"QListWidget {background-color:transparent;}")
        self.categoryList.setFrameShape(QFrame.StyledPanel)
        self.categoryList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.categoryList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.categoryList.setFlow(QListView.LeftToRight)
        self.categoryList.setSpacing(6)

        self.horizontalLayout_3.addWidget(self.categoryList)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.bookList = ComicListWidget(Search)
        self.bookList.setObjectName(u"bookList")

        self.verticalLayout.addWidget(self.bookList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sortKey = QComboBox(Search)
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.setObjectName(u"sortKey")
        self.sortKey.setEnabled(True)
        self.sortKey.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.sortKey)

        self.sortId = QComboBox(Search)
        self.sortId.addItem("")
        self.sortId.addItem("")
        self.sortId.setObjectName(u"sortId")
        self.sortId.setEnabled(True)

        self.horizontalLayout.addWidget(self.sortId)

        self.comboBox = QComboBox(Search)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.line_4 = QFrame(Search)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.label = QLabel(Search)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 30))
        self.label.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.label)

        self.line_5 = QFrame(Search)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_5)

        self.spinBox = QSpinBox(Search)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 0))
        self.spinBox.setStyleSheet(u"background-color:transparent;")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_6 = QFrame(Search)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_6)

        self.jumpPage = QPushButton(Search)
        self.jumpPage.setObjectName(u"jumpPage")
        self.jumpPage.setMinimumSize(QSize(60, 30))
        self.jumpPage.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.jumpPage)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Search)

        QMetaObject.connectSlotsByName(Search)
    # setupUi

    def retranslateUi(self, Search):
        Search.setWindowTitle(QCoreApplication.translate("Search", u"\u641c\u7d22", None))
        self.label_2.setText(QCoreApplication.translate("Search", u"\u641c\u7d22\uff1a", None))
        self.searchButton.setText(QCoreApplication.translate("Search", u"\u641c\u7d22", None))
        self.label_4.setText(QCoreApplication.translate("Search", u"\u5c4f\u853d\uff1a", None))
        self.sortKey.setItemText(0, QCoreApplication.translate("Search", u"\u66f4\u65b0\u65f6\u95f4", None))
        self.sortKey.setItemText(1, QCoreApplication.translate("Search", u"\u521b\u5efa\u65f6\u95f4", None))
        self.sortKey.setItemText(2, QCoreApplication.translate("Search", u"\u7231\u5fc3\u6570", None))
        self.sortKey.setItemText(3, QCoreApplication.translate("Search", u"\u89c2\u770b\u6570", None))
        self.sortKey.setItemText(4, QCoreApplication.translate("Search", u"\u7ae0\u8282\u6570", None))
        self.sortKey.setItemText(5, QCoreApplication.translate("Search", u"\u56fe\u7247\u6570", None))

        self.sortId.setItemText(0, QCoreApplication.translate("Search", u"\u964d\u5e8f", None))
        self.sortId.setItemText(1, QCoreApplication.translate("Search", u"\u5347\u5e8f", None))

        self.comboBox.setItemText(0, QCoreApplication.translate("Search", u"\u65b0\u5230\u65e7", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Search", u"\u65e7\u5230\u65b0", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Search", u"\u6700\u591a\u7231\u5fc3", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Search", u"\u6700\u591a\u7ec5\u58eb\u6307\u6570", None))

        self.label.setText(QCoreApplication.translate("Search", u"\u9875\uff1a0/0", None))
        self.jumpPage.setText(QCoreApplication.translate("Search", u"\u8df3\u8f6c", None))
    # retranslateUi

