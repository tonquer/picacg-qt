# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_local_favorite.ui'
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

class Ui_LocalFavorite(object):
    def setupUi(self, LocalFavorite):
        if not LocalFavorite.objectName():
            LocalFavorite.setObjectName(u"LocalFavorite")
        LocalFavorite.resize(628, 334)
        self.gridLayout_2 = QGridLayout(LocalFavorite)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bookList = ComicListWidget(LocalFavorite)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.msgLabel = QLabel(LocalFavorite)
        self.msgLabel.setObjectName(u"msgLabel")

        self.horizontalLayout.addWidget(self.msgLabel)

        self.sortKeyCombox = QComboBox(LocalFavorite)
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.setObjectName(u"sortKeyCombox")
        self.sortKeyCombox.setEnabled(True)
        self.sortKeyCombox.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.sortKeyCombox)

        self.sortIdCombox = QComboBox(LocalFavorite)
        self.sortIdCombox.addItem("")
        self.sortIdCombox.addItem("")
        self.sortIdCombox.setObjectName(u"sortIdCombox")
        self.sortIdCombox.setEnabled(True)

        self.horizontalLayout.addWidget(self.sortIdCombox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.line_2 = QFrame(LocalFavorite)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.nums = QLabel(LocalFavorite)
        self.nums.setObjectName(u"nums")
        self.nums.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(LocalFavorite)
        self.pages.setObjectName(u"pages")

        self.horizontalLayout.addWidget(self.pages)

        self.line = QFrame(LocalFavorite)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.line_4 = QFrame(LocalFavorite)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.spinBox = QSpinBox(LocalFavorite)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 30))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_3 = QFrame(LocalFavorite)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.jumpButton = QPushButton(LocalFavorite)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 2, 0, 1, 1)

        self.widget = QWidget(LocalFavorite)
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


        self.retranslateUi(LocalFavorite)
        self.jumpButton.clicked.connect(LocalFavorite.JumpPage)

        QMetaObject.connectSlotsByName(LocalFavorite)
    # setupUi

    def retranslateUi(self, LocalFavorite):
        LocalFavorite.setWindowTitle(QCoreApplication.translate("LocalFavorite", u"\u6536\u85cf", None))
        self.msgLabel.setText("")
        self.sortKeyCombox.setItemText(0, QCoreApplication.translate("LocalFavorite", u"\u6536\u85cf\u65f6\u95f4", None))

        self.sortIdCombox.setItemText(0, QCoreApplication.translate("LocalFavorite", u"\u964d\u5e8f", None))
        self.sortIdCombox.setItemText(1, QCoreApplication.translate("LocalFavorite", u"\u5347\u5e8f", None))

        self.nums.setText(QCoreApplication.translate("LocalFavorite", u"\u6536\u85cf\u6570\uff1a", None))
        self.pages.setText(QCoreApplication.translate("LocalFavorite", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("LocalFavorite", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("LocalFavorite", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("LocalFavorite", u"\u641c\u7d22\uff1a", None))
    # retranslateUi

