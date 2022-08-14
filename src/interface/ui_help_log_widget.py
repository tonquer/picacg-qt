# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_help_log_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFrame, QHBoxLayout,
    QPushButton, QRadioButton, QSizePolicy, QTextBrowser,
    QTextEdit, QToolButton, QVBoxLayout, QWidget)

class Ui_HelpLogWidget(object):
    def setupUi(self, HelpLogWidget):
        if not HelpLogWidget.objectName():
            HelpLogWidget.setObjectName(u"HelpLogWidget")
        HelpLogWidget.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(HelpLogWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.warnButton = QRadioButton(HelpLogWidget)
        self.buttonGroup = QButtonGroup(HelpLogWidget)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.warnButton)
        self.warnButton.setObjectName(u"warnButton")

        self.horizontalLayout.addWidget(self.warnButton)

        self.infoButton = QRadioButton(HelpLogWidget)
        self.buttonGroup.addButton(self.infoButton)
        self.infoButton.setObjectName(u"infoButton")
        self.infoButton.setChecked(True)

        self.horizontalLayout.addWidget(self.infoButton)

        self.debugButton = QRadioButton(HelpLogWidget)
        self.buttonGroup.addButton(self.debugButton)
        self.debugButton.setObjectName(u"debugButton")

        self.horizontalLayout.addWidget(self.debugButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.textBrowser = QTextBrowser(HelpLogWidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_2.addWidget(self.textBrowser)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.line = QFrame(HelpLogWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line)

        self.toolButton = QToolButton(HelpLogWidget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setArrowType(Qt.DownArrow)

        self.horizontalLayout_2.addWidget(self.toolButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.textEdit = QTextEdit(HelpLogWidget)
        self.textEdit.setObjectName(u"textEdit")

        self.horizontalLayout_3.addWidget(self.textEdit)

        self.runButton = QPushButton(HelpLogWidget)
        self.runButton.setObjectName(u"runButton")

        self.horizontalLayout_3.addWidget(self.runButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.retranslateUi(HelpLogWidget)

        QMetaObject.connectSlotsByName(HelpLogWidget)
    # setupUi

    def retranslateUi(self, HelpLogWidget):
        HelpLogWidget.setWindowTitle(QCoreApplication.translate("HelpLogWidget", u"\u63a7\u5236\u53f0", None))
        self.warnButton.setText(QCoreApplication.translate("HelpLogWidget", u"Warn", None))
        self.infoButton.setText(QCoreApplication.translate("HelpLogWidget", u"Info", None))
        self.debugButton.setText(QCoreApplication.translate("HelpLogWidget", u"Debug", None))
        self.toolButton.setText("")
        self.runButton.setText(QCoreApplication.translate("HelpLogWidget", u"\u8fd0\u884c\u4ee3\u7801", None))
    # retranslateUi

