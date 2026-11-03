# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_history.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_History(object):
    def setupUi(self, History):
        if not History.objectName():
            History.setObjectName(u"History")
        History.resize(683, 292)
        self.gridLayout_2 = QGridLayout(History)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bookList = ComicListWidget(History)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.widget = QWidget(History)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.updateCheck = QCheckBox(self.widget)
        self.updateCheck.setObjectName(u"updateCheck")

        self.horizontalLayout_3.addWidget(self.updateCheck)

        self.searchEdit = QLineEdit(self.widget)
        self.searchEdit.setObjectName(u"searchEdit")

        self.horizontalLayout_3.addWidget(self.searchEdit)


        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sortKey = QComboBox(History)
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.addItem("")
        self.sortKey.setObjectName(u"sortKey")
        self.sortKey.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.sortKey)

        self.sortId = QComboBox(History)
        self.sortId.addItem("")
        self.sortId.addItem("")
        self.sortId.setObjectName(u"sortId")
        self.sortId.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.sortId)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.line_2 = QFrame(History)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.nums = QLabel(History)
        self.nums.setObjectName(u"nums")
        self.nums.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(History)
        self.pages.setObjectName(u"pages")
        self.pages.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.pages)

        self.line = QFrame(History)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.spinBox = QSpinBox(History)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_3 = QFrame(History)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.jumpButton = QPushButton(History)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 2, 0, 1, 1)


        self.retranslateUi(History)
        self.jumpButton.clicked.connect(History.JumpPage)

        QMetaObject.connectSlotsByName(History)
    # setupUi

    def retranslateUi(self, History):
        History.setWindowTitle(QCoreApplication.translate("History", u"\u5386\u53f2\u8bb0\u5f55", None))
        self.label.setText(QCoreApplication.translate("History", u"\u641c\u7d22\uff1a", None))
        self.updateCheck.setText(QCoreApplication.translate("History", u"\u53ea\u770b\u6709\u66f4\u65b0", None))
        self.sortKey.setItemText(0, QCoreApplication.translate("History", u"\u6700\u8fd1\u9605\u8bfb", None))
        self.sortKey.setItemText(1, QCoreApplication.translate("History", u"\u66f4\u65b0\u65f6\u95f4", None))
        self.sortKey.setItemText(2, QCoreApplication.translate("History", u"\u521b\u5efa\u65f6\u95f4", None))
        self.sortKey.setItemText(3, QCoreApplication.translate("History", u"\u7231\u5fc3\u6570", None))
        self.sortKey.setItemText(4, QCoreApplication.translate("History", u"\u89c2\u770b\u6570", None))
        self.sortKey.setItemText(5, QCoreApplication.translate("History", u"\u7ae0\u8282\u6570", None))
        self.sortKey.setItemText(6, QCoreApplication.translate("History", u"\u56fe\u7247\u6570", None))

        self.sortId.setItemText(0, QCoreApplication.translate("History", u"\u964d\u5e8f", None))
        self.sortId.setItemText(1, QCoreApplication.translate("History", u"\u5347\u5e8f", None))

        self.nums.setText(QCoreApplication.translate("History", u"\u8bb0\u5f55\u6570\uff1a", None))
        self.pages.setText(QCoreApplication.translate("History", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("History", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("History", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

