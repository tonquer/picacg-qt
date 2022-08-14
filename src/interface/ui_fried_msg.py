# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_fried_msg.ui'
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
    QListWidgetItem, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)

from component.label.auto_picture_label import AutoPictureLabel
from component.label.head_label import HeadLabel
from component.list.user_list_widget import UserListWidget

class Ui_FriedMsg(object):
    def setupUi(self, FriedMsg):
        if not FriedMsg.objectName():
            FriedMsg.setObjectName(u"FriedMsg")
        FriedMsg.resize(530, 591)
        self.gridLayout_2 = QGridLayout(FriedMsg)
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 1, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.picLabel = HeadLabel(FriedMsg)
        self.picLabel.setObjectName(u"picLabel")
        self.picLabel.setMinimumSize(QSize(100, 100))
        self.picLabel.setMaximumSize(QSize(100, 100))

        self.verticalLayout.addWidget(self.picLabel, 0, Qt.AlignTop)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.nameLabel = QLabel(FriedMsg)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setMinimumSize(QSize(0, 20))
        self.nameLabel.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(12)
        self.nameLabel.setFont(font)

        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, -1, 4, -1)
        self.indexLabel = QLabel(FriedMsg)
        self.indexLabel.setObjectName(u"indexLabel")

        self.horizontalLayout.addWidget(self.indexLabel)

        self.levelLabel = QLabel(FriedMsg)
        self.levelLabel.setObjectName(u"levelLabel")
        self.levelLabel.setMinimumSize(QSize(0, 20))
        self.levelLabel.setMaximumSize(QSize(16777215, 20))
        self.levelLabel.setStyleSheet(u"background:#eeA2A4;")

        self.horizontalLayout.addWidget(self.levelLabel)

        self.titleLabel = QLabel(FriedMsg)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setMinimumSize(QSize(0, 20))
        self.titleLabel.setMaximumSize(QSize(16777215, 20))
        self.titleLabel.setStyleSheet(u"background:#eeA2A4;")

        self.horizontalLayout.addWidget(self.titleLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.widget = QWidget(FriedMsg)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.commentLabel = QLabel(self.widget)
        self.commentLabel.setObjectName(u"commentLabel")
        self.commentLabel.setFont(font)

        self.verticalLayout_3.addWidget(self.commentLabel)

        self.replayLabel = AutoPictureLabel(self.widget)
        self.replayLabel.setObjectName(u"replayLabel")
        self.replayLabel.setFont(font)

        self.verticalLayout_3.addWidget(self.replayLabel)

        self.infoLabel = QLabel(self.widget)
        self.infoLabel.setObjectName(u"infoLabel")
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setUnderline(False)
        self.infoLabel.setFont(font1)
        self.infoLabel.setStyleSheet(u"color: #999999;")
        self.infoLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.infoLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.likeButton = QToolButton(self.widget)
        self.likeButton.setObjectName(u"likeButton")
        self.likeButton.setStyleSheet(u"background-color:transparent;")

        self.horizontalLayout_2.addWidget(self.likeButton)

        self.commentButton = QToolButton(self.widget)
        self.commentButton.setObjectName(u"commentButton")
        self.commentButton.setStyleSheet(u"background-color:transparent;")

        self.horizontalLayout_2.addWidget(self.commentButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.listWidget = UserListWidget(self.widget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMinimumSize(QSize(0, 400))
        self.listWidget.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
"QListWidget::item { border-bottom: 1px solid black; }")

        self.verticalLayout_3.addWidget(self.listWidget)


        self.gridLayout.addWidget(self.widget, 4, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)


        self.retranslateUi(FriedMsg)
        self.commentButton.clicked.connect(FriedMsg.OpenComment)

        QMetaObject.connectSlotsByName(FriedMsg)
    # setupUi

    def retranslateUi(self, FriedMsg):
        FriedMsg.setWindowTitle(QCoreApplication.translate("FriedMsg", u"Form", None))
        self.picLabel.setText(QCoreApplication.translate("FriedMsg", u"TextLabel", None))
        self.nameLabel.setText(QCoreApplication.translate("FriedMsg", u"TextLabel", None))
        self.indexLabel.setText(QCoreApplication.translate("FriedMsg", u"X\u697c", None))
        self.levelLabel.setText(QCoreApplication.translate("FriedMsg", u"LV", None))
        self.titleLabel.setText(QCoreApplication.translate("FriedMsg", u"TextLabel", None))
        self.commentLabel.setText(QCoreApplication.translate("FriedMsg", u"TextLabel", None))
        self.replayLabel.setText(QCoreApplication.translate("FriedMsg", u"TextLabel", None))
        self.infoLabel.setText(QCoreApplication.translate("FriedMsg", u"TextLabel", None))
        self.likeButton.setText(QCoreApplication.translate("FriedMsg", u"(0)", None))
        self.commentButton.setText(QCoreApplication.translate("FriedMsg", u"(0)", None))
    # retranslateUi

