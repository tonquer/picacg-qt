# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_exit.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QHBoxLayout,
    QPushButton, QRadioButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Exit(object):
    def setupUi(self, Exit):
        if not Exit.objectName():
            Exit.setObjectName(u"Exit")
        Exit.resize(400, 231)
        self.verticalLayout = QVBoxLayout(Exit)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Exit)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radioButton1 = QRadioButton(self.widget)
        self.buttonGroup = QButtonGroup(Exit)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton1)
        self.radioButton1.setObjectName(u"radioButton1")
        self.radioButton1.setChecked(True)

        self.verticalLayout_2.addWidget(self.radioButton1)

        self.radioButton2 = QRadioButton(self.widget)
        self.buttonGroup.addButton(self.radioButton2)
        self.radioButton2.setObjectName(u"radioButton2")
        self.radioButton2.setChecked(False)

        self.verticalLayout_2.addWidget(self.radioButton2)

        self.checkBox = QCheckBox(self.widget)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout_2.addWidget(self.checkBox)


        self.verticalLayout.addWidget(self.widget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.button = QPushButton(Exit)
        self.button.setObjectName(u"button")
        self.button.setMaximumSize(QSize(150, 30))
        self.button.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.button)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Exit)

        QMetaObject.connectSlotsByName(Exit)
    # setupUi

    def retranslateUi(self, Exit):
        Exit.setWindowTitle(QCoreApplication.translate("Exit", u"Form", None))
        self.radioButton1.setText(QCoreApplication.translate("Exit", u"\u9000\u51fa", None))
        self.radioButton2.setText(QCoreApplication.translate("Exit", u"\u6700\u5c0f\u5316\u5230\u4efb\u52a1\u680f", None))
        self.checkBox.setText(QCoreApplication.translate("Exit", u"\u4e0d\u5728\u6bcf\u6b21\u5f39\u51fa\u8be5\u7a97\u53e3\uff08\u53ef\u5728\u8bbe\u7f6e\u4e2d\u8bbe\u7f6e\uff09", None))
        self.button.setText(QCoreApplication.translate("Exit", u"\u786e\u5b9a", None))
#if QT_CONFIG(shortcut)
        self.button.setShortcut(QCoreApplication.translate("Exit", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

