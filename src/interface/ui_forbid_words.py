# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_forbid_words.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ForbidWords(object):
    def setupUi(self, ForbidWords):
        if not ForbidWords.objectName():
            ForbidWords.setObjectName(u"ForbidWords")
        ForbidWords.resize(400, 300)
        self.verticalLayout = QVBoxLayout(ForbidWords)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.categoryBox = QCheckBox(ForbidWords)
        self.categoryBox.setObjectName(u"categoryBox")
        self.categoryBox.setChecked(True)

        self.horizontalLayout.addWidget(self.categoryBox)

        self.tagBox = QCheckBox(ForbidWords)
        self.tagBox.setObjectName(u"tagBox")

        self.horizontalLayout.addWidget(self.tagBox)

        self.titleBox = QCheckBox(ForbidWords)
        self.titleBox.setObjectName(u"titleBox")

        self.horizontalLayout.addWidget(self.titleBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.editButton = QPushButton(ForbidWords)
        self.editButton.setObjectName(u"editButton")

        self.horizontalLayout.addWidget(self.editButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = QListWidget(ForbidWords)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.saveButton = QPushButton(ForbidWords)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_2.addWidget(self.saveButton)

        self.closeButton = QPushButton(ForbidWords)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout_2.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(ForbidWords)

        QMetaObject.connectSlotsByName(ForbidWords)
    # setupUi

    def retranslateUi(self, ForbidWords):
        ForbidWords.setWindowTitle(QCoreApplication.translate("ForbidWords", u"Form", None))
        self.categoryBox.setText(QCoreApplication.translate("ForbidWords", u"\u5206\u7c7b\u5c4f\u853d", None))
        self.tagBox.setText(QCoreApplication.translate("ForbidWords", u"Tag\u5c4f\u853d", None))
        self.titleBox.setText(QCoreApplication.translate("ForbidWords", u"\u6807\u9898\u5c4f\u853d", None))
        self.editButton.setText(QCoreApplication.translate("ForbidWords", u"\u7f16\u8f91", None))
        self.saveButton.setText(QCoreApplication.translate("ForbidWords", u"\u4fdd\u5b58", None))
        self.closeButton.setText(QCoreApplication.translate("ForbidWords", u"\u53d6\u6d88", None))
    # retranslateUi

