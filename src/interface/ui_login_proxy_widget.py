# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_login_proxy_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QCommandLinkButton,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_LoginProxyWidget(object):
    def setupUi(self, LoginProxyWidget):
        if not LoginProxyWidget.objectName():
            LoginProxyWidget.setObjectName(u"LoginProxyWidget")
        LoginProxyWidget.resize(455, 418)
        LoginProxyWidget.setMinimumSize(QSize(450, 0))
        self.gridLayout = QGridLayout(LoginProxyWidget)
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.httpsBox = QCheckBox(LoginProxyWidget)
        self.httpsBox.setObjectName(u"httpsBox")
        self.httpsBox.setChecked(True)

        self.horizontalLayout_9.addWidget(self.httpsBox)


        self.gridLayout.addLayout(self.horizontalLayout_9, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_3 = QLabel(LoginProxyWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_8.addWidget(self.label_3)

        self.commandLinkButton = QCommandLinkButton(LoginProxyWidget)
        self.commandLinkButton.setObjectName(u"commandLinkButton")

        self.horizontalLayout_8.addWidget(self.commandLinkButton)


        self.gridLayout.addLayout(self.horizontalLayout_8, 7, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_11 = QLabel(LoginProxyWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.label_11)

        self.cdnIp = QLineEdit(LoginProxyWidget)
        self.cdnIp.setObjectName(u"cdnIp")

        self.horizontalLayout_6.addWidget(self.cdnIp)


        self.gridLayout.addLayout(self.horizontalLayout_6, 9, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.radioButton_1 = QRadioButton(LoginProxyWidget)
        self.buttonGroup = QButtonGroup(LoginProxyWidget)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton_1)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setChecked(True)

        self.horizontalLayout_5.addWidget(self.radioButton_1)

        self.label1 = QLabel(LoginProxyWidget)
        self.label1.setObjectName(u"label1")
        self.label1.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label1)

        self.label2 = QLabel(LoginProxyWidget)
        self.label2.setObjectName(u"label2")
        self.label2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label2)


        self.gridLayout.addLayout(self.horizontalLayout_5, 4, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 11, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.testSpeedButton = QPushButton(LoginProxyWidget)
        self.testSpeedButton.setObjectName(u"testSpeedButton")

        self.horizontalLayout_2.addWidget(self.testSpeedButton)

        self.label_2 = QLabel(LoginProxyWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_4 = QLabel(LoginProxyWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_4)


        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.proxyBox = QCheckBox(LoginProxyWidget)
        self.proxyBox.setObjectName(u"proxyBox")

        self.horizontalLayout.addWidget(self.proxyBox)

        self.line = QFrame(LoginProxyWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label = QLabel(LoginProxyWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.httpLine = QLineEdit(LoginProxyWidget)
        self.httpLine.setObjectName(u"httpLine")

        self.horizontalLayout.addWidget(self.httpLine)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radioButton_2 = QRadioButton(LoginProxyWidget)
        self.buttonGroup.addButton(self.radioButton_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_4.addWidget(self.radioButton_2)

        self.label3 = QLabel(LoginProxyWidget)
        self.label3.setObjectName(u"label3")
        self.label3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label3)

        self.label4 = QLabel(LoginProxyWidget)
        self.label4.setObjectName(u"label4")
        self.label4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label4)


        self.gridLayout.addLayout(self.horizontalLayout_4, 5, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.radioButton_4 = QRadioButton(LoginProxyWidget)
        self.buttonGroup.addButton(self.radioButton_4)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.horizontalLayout_7.addWidget(self.radioButton_4)

        self.label7 = QLabel(LoginProxyWidget)
        self.label7.setObjectName(u"label7")
        self.label7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label7)

        self.label8 = QLabel(LoginProxyWidget)
        self.label8.setObjectName(u"label8")
        self.label8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label8)


        self.gridLayout.addLayout(self.horizontalLayout_7, 10, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton_3 = QRadioButton(LoginProxyWidget)
        self.buttonGroup.addButton(self.radioButton_3)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.horizontalLayout_3.addWidget(self.radioButton_3)

        self.label5 = QLabel(LoginProxyWidget)
        self.label5.setObjectName(u"label5")
        self.label5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label5)

        self.label6 = QLabel(LoginProxyWidget)
        self.label6.setObjectName(u"label6")
        self.label6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label6)


        self.gridLayout.addLayout(self.horizontalLayout_3, 6, 0, 1, 1)


        self.retranslateUi(LoginProxyWidget)
        self.testSpeedButton.clicked.connect(LoginProxyWidget.SpeedTest)

        QMetaObject.connectSlotsByName(LoginProxyWidget)
    # setupUi

    def retranslateUi(self, LoginProxyWidget):
        LoginProxyWidget.setWindowTitle(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406\u8bbe\u7f6e", None))
        self.httpsBox.setText(QCoreApplication.translate("LoginProxyWidget", u"\u542f\u7528HTTPS", None))
        self.label_3.setText(QCoreApplication.translate("LoginProxyWidget", u"CDN\u8bbe\u7f6e\u8bf7\u770b\u8bf4\u660e\u83b7\u53d6", None))
        self.commandLinkButton.setText(QCoreApplication.translate("LoginProxyWidget", u"\u8bf4\u660e", None))
        self.label_11.setText(QCoreApplication.translate("LoginProxyWidget", u" CDN\u7684IP\u5730\u5740 ", None))
        self.radioButton_1.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d411", None))
        self.label1.setText("")
        self.label2.setText("")
        self.testSpeedButton.setText(QCoreApplication.translate("LoginProxyWidget", u"\u6d4b\u901f", None))
        self.label_2.setText(QCoreApplication.translate("LoginProxyWidget", u"\u76f4\u8fde", None))
        self.label_4.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406", None))
        self.proxyBox.setText(QCoreApplication.translate("LoginProxyWidget", u"\u542f\u7528\u4ee3\u7406", None))
        self.label.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406\u5730\u5740", None))
        self.radioButton_2.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d412", None))
        self.label3.setText("")
        self.label4.setText("")
        self.radioButton_4.setText(QCoreApplication.translate("LoginProxyWidget", u"CDN\u5206\u6d41", None))
        self.label7.setText("")
        self.label8.setText("")
        self.radioButton_3.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d413", None))
        self.label5.setText("")
        self.label6.setText("")
    # retranslateUi

