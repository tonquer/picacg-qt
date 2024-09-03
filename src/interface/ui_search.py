# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_search.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from component.line_edit.search_line_edit import SearchLineEdit
from component.list.comic_list_widget import ComicListWidget

class Ui_Search(object):
    def setupUi(self, Search):
        if not Search.objectName():
            Search.setObjectName(u"Search")
        Search.resize(740, 459)
        Search.setMinimumSize(QSize(80, 0))
        self.verticalLayout = QVBoxLayout(Search)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.searchTab = QLabel(Search)
        self.searchTab.setObjectName(u"searchTab")
        self.searchTab.setEnabled(True)
        self.searchTab.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.verticalLayout.addWidget(self.searchTab)

        self.searchWidget = QWidget(Search)
        self.searchWidget.setObjectName(u"searchWidget")
        self.verticalLayout_3 = QVBoxLayout(self.searchWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.searchLayout = QHBoxLayout()
        self.searchLayout.setObjectName(u"searchLayout")
        self.searchLabel1 = QLabel(self.searchWidget)
        self.searchLabel1.setObjectName(u"searchLabel1")
        self.searchLabel1.setMinimumSize(QSize(60, 0))
        self.searchLabel1.setMaximumSize(QSize(60, 40))

        self.searchLayout.addWidget(self.searchLabel1)

        self.searchLabel = QLabel(self.searchWidget)
        self.searchLabel.setObjectName(u"searchLabel")
        self.searchLabel.setMinimumSize(QSize(20, 0))
        self.searchLabel.setMaximumSize(QSize(20, 16777215))
        self.searchLabel.setToolTipDuration(-1)
        self.searchLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.searchLayout.addWidget(self.searchLabel)

        self.lineEdit = SearchLineEdit(self.searchWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(40, 40))
        self.lineEdit.setClearButtonEnabled(True)

        self.searchLayout.addWidget(self.lineEdit)

        self.searchButton = QPushButton(self.searchWidget)
        self.searchButton.setObjectName(u"searchButton")

        self.searchLayout.addWidget(self.searchButton)


        self.verticalLayout_3.addLayout(self.searchLayout)


        self.verticalLayout.addWidget(self.searchWidget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(Search)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(80, 40))

        self.horizontalLayout_6.addWidget(self.label_3)

        self.unfoldButton = QPushButton(Search)
        self.unfoldButton.setObjectName(u"unfoldButton")

        self.horizontalLayout_6.addWidget(self.unfoldButton)

        self.selectAllButton = QPushButton(Search)
        self.selectAllButton.setObjectName(u"selectAllButton")

        self.horizontalLayout_6.addWidget(self.selectAllButton)

        self.saveButton = QPushButton(Search)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_6.addWidget(self.saveButton)

        self.categoryNum = QLabel(Search)
        self.categoryNum.setObjectName(u"categoryNum")

        self.horizontalLayout_6.addWidget(self.categoryNum)

        self.hideLabel = QLabel(Search)
        self.hideLabel.setObjectName(u"hideLabel")

        self.horizontalLayout_6.addWidget(self.hideLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.widget = QWidget(Search)
        self.widget.setObjectName(u"widget")

        self.verticalLayout_2.addWidget(self.widget)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

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

        self.someDownButton = QPushButton(Search)
        self.someDownButton.setObjectName(u"someDownButton")

        self.horizontalLayout.addWidget(self.someDownButton)

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
        self.searchTab.setText("")
#if QT_CONFIG(tooltip)
        self.searchLabel1.setToolTip(QCoreApplication.translate("Search", u"<html><head/><body><p>\u641c\u5bfb\u7684\u6700\u4f73\u59ff\u52bf?</p><p>\u3010\u5305\u542b\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][+]\u4eba\u59bb,\u4ec5\u663e\u793a\u5168\u5f69\u4e14\u662f\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 +\u4eba\u59bb<br/></p><p>\u3010\u6392\u9664\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][]\u4eba\u59bb,\u663e\u793a\u5168\u5f69\u5e76\u6392\u9664\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 -\u4eba\u59bb<br/></p><p>\u3010\u6211\u90fd\u8981\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c]\u4eba\u59bb,\u4f1a\u663e\u793a\u6240\u6709\u5305\u542b\u5168\u5f69\u53ca\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 \u4eba\u59bb</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.searchLabel1.setText(QCoreApplication.translate("Search", u"\u641c\u7d22\uff1a", None))
#if QT_CONFIG(tooltip)
        self.searchLabel.setToolTip(QCoreApplication.translate("Search", u"<html><head/><body><p>\u641c\u5bfb\u7684\u6700\u4f73\u59ff\u52bf?</p><p>\u3010\u5305\u542b\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][+]\u4eba\u59bb,\u4ec5\u663e\u793a\u5168\u5f69\u4e14\u662f\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 +\u4eba\u59bb<br/></p><p>\u3010\u6392\u9664\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][]\u4eba\u59bb,\u663e\u793a\u5168\u5f69\u5e76\u6392\u9664\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 -\u4eba\u59bb<br/></p><p>\u3010\u6211\u90fd\u8981\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c]\u4eba\u59bb,\u4f1a\u663e\u793a\u6240\u6709\u5305\u542b\u5168\u5f69\u53ca\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 \u4eba\u59bb</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.searchLabel.setText(QCoreApplication.translate("Search", u"?", None))
        self.searchButton.setText(QCoreApplication.translate("Search", u"\u641c\u7d22", None))
        self.label_3.setText(QCoreApplication.translate("Search", u"\u5206\u7c7b\u8fc7\u6ee4\uff1a", None))
        self.unfoldButton.setText(QCoreApplication.translate("Search", u"\u5c55\u5f00", None))
        self.selectAllButton.setText(QCoreApplication.translate("Search", u"\u5168\u9009", None))
        self.saveButton.setText(QCoreApplication.translate("Search", u"\u786e\u5b9a", None))
        self.categoryNum.setText("")
        self.hideLabel.setText("")
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

        self.someDownButton.setText(QCoreApplication.translate("Search", u"\u6279\u91cf\u4e0b\u8f7d", None))
        self.label.setText(QCoreApplication.translate("Search", u"\u9875\uff1a0/0", None))
        self.jumpPage.setText(QCoreApplication.translate("Search", u"\u8df3\u8f6c", None))
    # retranslateUi

