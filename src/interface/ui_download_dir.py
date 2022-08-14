# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_download_dir.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_DownloadDir(object):
    def setupUi(self, DownloadDir):
        if not DownloadDir.objectName():
            DownloadDir.setObjectName(u"DownloadDir")
        DownloadDir.resize(401, 300)
        self.verticalLayout = QVBoxLayout(DownloadDir)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label = QLabel(DownloadDir)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(DownloadDir)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(DownloadDir)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(300, 0))

        self.horizontalLayout.addWidget(self.lineEdit)

        self.selectDir = QPushButton(DownloadDir)
        self.selectDir.setObjectName(u"selectDir")

        self.horizontalLayout.addWidget(self.selectDir)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(DownloadDir)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.downloadDir = QLabel(DownloadDir)
        self.downloadDir.setObjectName(u"downloadDir")

        self.gridLayout.addWidget(self.downloadDir, 0, 1, 1, 1)

        self.label_5 = QLabel(DownloadDir)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.cacheDir = QLabel(DownloadDir)
        self.cacheDir.setObjectName(u"cacheDir")

        self.gridLayout.addWidget(self.cacheDir, 1, 1, 1, 1)

        self.label_7 = QLabel(DownloadDir)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)

        self.chatDir = QLabel(DownloadDir)
        self.chatDir.setObjectName(u"chatDir")

        self.gridLayout.addWidget(self.chatDir, 2, 1, 1, 1)

        self.label_4 = QLabel(DownloadDir)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.waifu2xDir = QLabel(DownloadDir)
        self.waifu2xDir.setObjectName(u"waifu2xDir")

        self.gridLayout.addWidget(self.waifu2xDir, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.saveDir = QPushButton(DownloadDir)
        self.saveDir.setObjectName(u"saveDir")

        self.verticalLayout.addWidget(self.saveDir)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(DownloadDir)

        QMetaObject.connectSlotsByName(DownloadDir)
    # setupUi

    def retranslateUi(self, DownloadDir):
        DownloadDir.setWindowTitle(QCoreApplication.translate("DownloadDir", u"Form", None))
        self.label.setText(QCoreApplication.translate("DownloadDir", u"\u4f60\u5fc5\u987b\u8bbe\u7f6e\u4e0b\u8f7d\u4e0e\u7f13\u5b58\u7684\u8def\u5f84\u624d\u80fd\u4f7f\u7528", None))
        self.label_2.setText(QCoreApplication.translate("DownloadDir", u"\u76ee\u5f55", None))
        self.selectDir.setText(QCoreApplication.translate("DownloadDir", u"...", None))
        self.label_3.setText(QCoreApplication.translate("DownloadDir", u"\u4e0b\u8f7d:", None))
        self.downloadDir.setText("")
        self.label_5.setText(QCoreApplication.translate("DownloadDir", u"\u7f13\u5b58:", None))
        self.cacheDir.setText("")
        self.label_7.setText(QCoreApplication.translate("DownloadDir", u"\u804a\u5929:", None))
        self.chatDir.setText("")
        self.label_4.setText(QCoreApplication.translate("DownloadDir", u"waifu2x\u7f13\u5b58:", None))
        self.waifu2xDir.setText("")
        self.saveDir.setText(QCoreApplication.translate("DownloadDir", u"\u4fdd\u5b58", None))
    # retranslateUi

