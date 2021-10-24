# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QGridLayout,
    QLabel, QSizePolicy, QWidget)

class Ui_Test(object):
    def setupUi(self, Test):
        if not Test.objectName():
            Test.setObjectName(u"Test")
        Test.resize(411, 301)
        Test.setAcceptDrops(False)
        self.gridLayout = QGridLayout(Test)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Test)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.graphicsView = QGraphicsView(self.frame)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(10, 50, 256, 192))
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(250, 140, 54, 12))

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Test)

        QMetaObject.connectSlotsByName(Test)
    # setupUi

    def retranslateUi(self, Test):
        Test.setWindowTitle(QCoreApplication.translate("Test", u"Form", None))
        self.label.setText(QCoreApplication.translate("Test", u"TextLabel", None))
    # retranslateUi

