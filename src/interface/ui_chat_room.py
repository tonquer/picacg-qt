# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_chat_room.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget)

from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_ChatRoom(object):
    def setupUi(self, ChatRoom):
        if not ChatRoom.objectName():
            ChatRoom.setObjectName(u"ChatRoom")
        ChatRoom.resize(530, 582)
        self.gridLayout = QGridLayout(ChatRoom)
        self.gridLayout.setObjectName(u"gridLayout")
        self.atLabel = QPushButton(ChatRoom)
        self.atLabel.setObjectName(u"atLabel")
        self.atLabel.setFlat(True)

        self.gridLayout.addWidget(self.atLabel, 3, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.nameLabel = QLabel(ChatRoom)
        self.nameLabel.setObjectName(u"nameLabel")

        self.horizontalLayout_3.addWidget(self.nameLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.label = QLabel(ChatRoom)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.onlineNum = QLabel(ChatRoom)
        self.onlineNum.setObjectName(u"onlineNum")

        self.horizontalLayout_3.addWidget(self.onlineNum)

        self.numLabel = QLabel(ChatRoom)
        self.numLabel.setObjectName(u"numLabel")

        self.horizontalLayout_3.addWidget(self.numLabel)


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.gridLayout.addLayout(self.horizontalLayout, 7, 0, 1, 1)

        self.scrollArea = SmoothScrollArea(ChatRoom)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 510, 168))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 2, 0, 1, 1)

        self.replyLabel = QPushButton(ChatRoom)
        self.replyLabel.setObjectName(u"replyLabel")
        self.replyLabel.setAutoExclusive(False)
        self.replyLabel.setFlat(True)

        self.gridLayout.addWidget(self.replyLabel, 4, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.textEdit = QTextEdit(ChatRoom)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMaximumSize(QSize(16777215, 100))
        font = QFont()
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet(u"background-color:transparent;")

        self.horizontalLayout_2.addWidget(self.textEdit)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton = QPushButton(ChatRoom)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.pushButton)

        self.picButton = QPushButton(ChatRoom)
        self.picButton.setObjectName(u"picButton")
        self.picButton.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.picButton)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.sendButton = QPushButton(ChatRoom)
        self.sendButton.setObjectName(u"sendButton")
        self.sendButton.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_4.addWidget(self.sendButton)

        self.toolButton = QPushButton(ChatRoom)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_4.addWidget(self.toolButton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 0, 1, 1)

        self.listWidget = QListWidget(ChatRoom)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMaximumSize(QSize(16777215, 100))
        self.listWidget.setStyleSheet(u"background-color:transparent;")

        self.gridLayout.addWidget(self.listWidget, 5, 0, 1, 1)

        self.widget = QWidget(ChatRoom)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 40))

        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)


        self.retranslateUi(ChatRoom)
        self.sendButton.clicked.connect(ChatRoom.SendMsg)
        self.picButton.clicked.connect(ChatRoom.OpenPicture)
        self.atLabel.clicked.connect(ChatRoom.SetEnable1)
        self.replyLabel.clicked.connect(ChatRoom.SetEnable2)
        self.pushButton.clicked.connect(ChatRoom.OpenIcon)

        QMetaObject.connectSlotsByName(ChatRoom)
    # setupUi

    def retranslateUi(self, ChatRoom):
        ChatRoom.setWindowTitle(QCoreApplication.translate("ChatRoom", u"\u804a\u5929\u5ba4", None))
        self.atLabel.setText(QCoreApplication.translate("ChatRoom", u"PushButton", None))
        self.nameLabel.setText(QCoreApplication.translate("ChatRoom", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("ChatRoom", u"\u5728\u7ebf\u4eba\u6570\uff1a", None))
        self.onlineNum.setText(QCoreApplication.translate("ChatRoom", u"0", None))
        self.numLabel.setText("")
        self.replyLabel.setText(QCoreApplication.translate("ChatRoom", u"PushButton", None))
        self.pushButton.setText(QCoreApplication.translate("ChatRoom", u"\u8868\u60c5", None))
        self.picButton.setText(QCoreApplication.translate("ChatRoom", u"\u56fe\u7247", None))
        self.sendButton.setText(QCoreApplication.translate("ChatRoom", u"\u53d1\u9001", None))
        self.toolButton.setText("")
    # retranslateUi

