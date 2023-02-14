# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_local.ui'
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
    QHBoxLayout, QLabel, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_Local(object):
    def setupUi(self, Local):
        if not Local.objectName():
            Local.setObjectName(u"Local")
        Local.resize(628, 334)
        self.gridLayout_2 = QGridLayout(Local)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.toolButton = QPushButton(Local)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_2.addWidget(self.toolButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bookList = ComicListWidget(Local)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 2, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.msgLabel = QLabel(Local)
        self.msgLabel.setObjectName(u"msgLabel")

        self.horizontalLayout.addWidget(self.msgLabel)

        self.sortKeyCombox = QComboBox(Local)
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.setObjectName(u"sortKeyCombox")
        self.sortKeyCombox.setEnabled(True)
        self.sortKeyCombox.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.sortKeyCombox)

        self.sortIdCombox = QComboBox(Local)
        self.sortIdCombox.addItem("")
        self.sortIdCombox.addItem("")
        self.sortIdCombox.setObjectName(u"sortIdCombox")
        self.sortIdCombox.setEnabled(True)

        self.horizontalLayout.addWidget(self.sortIdCombox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.line_2 = QFrame(Local)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.nums = QLabel(Local)
        self.nums.setObjectName(u"nums")
        self.nums.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(Local)
        self.pages.setObjectName(u"pages")

        self.horizontalLayout.addWidget(self.pages)

        self.line = QFrame(Local)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.line_4 = QFrame(Local)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.spinBox = QSpinBox(Local)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 30))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_3 = QFrame(Local)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.jumpButton = QPushButton(Local)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 3, 0, 1, 1)


        self.retranslateUi(Local)
        self.jumpButton.clicked.connect(Local.JumpPage)

        QMetaObject.connectSlotsByName(Local)
    # setupUi

    def retranslateUi(self, Local):
        Local.setWindowTitle(QCoreApplication.translate("Local", u"\u672c\u5730\u6f2b\u753b", None))
        self.toolButton.setText(QCoreApplication.translate("Local", u"\u5bfc\u5165", None))
        self.msgLabel.setText("")
        self.sortKeyCombox.setItemText(0, QCoreApplication.translate("Local", u"\u4e0a\u6b21\u9605\u8bfb\u65f6\u95f4", None))
        self.sortKeyCombox.setItemText(1, QCoreApplication.translate("Local", u"\u6dfb\u52a0\u65f6\u95f4", None))

        self.sortIdCombox.setItemText(0, QCoreApplication.translate("Local", u"\u964d\u5e8f", None))
        self.sortIdCombox.setItemText(1, QCoreApplication.translate("Local", u"\u5347\u5e8f", None))

        self.nums.setText(QCoreApplication.translate("Local", u"\u6536\u85cf\u6570\uff1a", None))
        self.pages.setText(QCoreApplication.translate("Local", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("Local", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("Local", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

