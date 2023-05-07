# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_favorite.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_Favorite(object):
    def setupUi(self, Favorite):
        if not Favorite.objectName():
            Favorite.setObjectName(u"Favorite")
        Favorite.resize(628, 334)
        self.gridLayout_2 = QGridLayout(Favorite)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bookList = ComicListWidget(Favorite)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.msgLabel = QLabel(Favorite)
        self.msgLabel.setObjectName(u"msgLabel")

        self.horizontalLayout.addWidget(self.msgLabel)

        self.sortKeyCombox = QComboBox(Favorite)
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.setObjectName(u"sortKeyCombox")
        self.sortKeyCombox.setEnabled(True)
        self.sortKeyCombox.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.sortKeyCombox)

        self.sortIdCombox = QComboBox(Favorite)
        self.sortIdCombox.addItem("")
        self.sortIdCombox.addItem("")
        self.sortIdCombox.setObjectName(u"sortIdCombox")
        self.sortIdCombox.setEnabled(True)

        self.horizontalLayout.addWidget(self.sortIdCombox)

        self.sortCombox = QComboBox(Favorite)
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.setObjectName(u"sortCombox")

        self.horizontalLayout.addWidget(self.sortCombox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.someDownButton = QPushButton(Favorite)
        self.someDownButton.setObjectName(u"someDownButton")

        self.horizontalLayout.addWidget(self.someDownButton)

        self.line_2 = QFrame(Favorite)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.nums = QLabel(Favorite)
        self.nums.setObjectName(u"nums")
        self.nums.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(Favorite)
        self.pages.setObjectName(u"pages")

        self.horizontalLayout.addWidget(self.pages)

        self.line = QFrame(Favorite)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.line_4 = QFrame(Favorite)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.spinBox = QSpinBox(Favorite)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 30))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_3 = QFrame(Favorite)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.jumpButton = QPushButton(Favorite)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 2, 0, 1, 1)

        self.widget = QWidget(Favorite)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)


        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)


        self.retranslateUi(Favorite)
        self.jumpButton.clicked.connect(Favorite.JumpPage)

        QMetaObject.connectSlotsByName(Favorite)
    # setupUi

    def retranslateUi(self, Favorite):
        Favorite.setWindowTitle(QCoreApplication.translate("Favorite", u"\u6536\u85cf", None))
        self.msgLabel.setText("")
        self.sortKeyCombox.setItemText(0, QCoreApplication.translate("Favorite", u"\u66f4\u65b0\u65f6\u95f4", None))
        self.sortKeyCombox.setItemText(1, QCoreApplication.translate("Favorite", u"\u521b\u5efa\u65f6\u95f4", None))
        self.sortKeyCombox.setItemText(2, QCoreApplication.translate("Favorite", u"\u7231\u5fc3\u6570", None))
        self.sortKeyCombox.setItemText(3, QCoreApplication.translate("Favorite", u"\u89c2\u770b\u6570", None))
        self.sortKeyCombox.setItemText(4, QCoreApplication.translate("Favorite", u"\u7ae0\u8282\u6570", None))
        self.sortKeyCombox.setItemText(5, QCoreApplication.translate("Favorite", u"\u56fe\u7247\u6570", None))

        self.sortIdCombox.setItemText(0, QCoreApplication.translate("Favorite", u"\u964d\u5e8f", None))
        self.sortIdCombox.setItemText(1, QCoreApplication.translate("Favorite", u"\u5347\u5e8f", None))

        self.sortCombox.setItemText(0, QCoreApplication.translate("Favorite", u"\u65b0\u5230\u65e7", None))
        self.sortCombox.setItemText(1, QCoreApplication.translate("Favorite", u"\u65e7\u5230\u65b0", None))
        self.sortCombox.setItemText(2, QCoreApplication.translate("Favorite", u"\u6700\u591a\u7231\u5fc3", None))
        self.sortCombox.setItemText(3, QCoreApplication.translate("Favorite", u"\u6700\u591a\u7ec5\u58eb\u6307\u6570", None))

        self.someDownButton.setText(QCoreApplication.translate("Favorite", u"\u6279\u91cf\u4e0b\u8f7d", None))
        self.nums.setText(QCoreApplication.translate("Favorite", u"\u6536\u85cf\u6570\uff1a", None))
        self.pages.setText(QCoreApplication.translate("Favorite", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("Favorite", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("Favorite", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("Favorite", u"\u641c\u7d22\uff1a", None))
    # retranslateUi

