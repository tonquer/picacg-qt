# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_proxy.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_LoginProxy(object):
    def setupUi(self, LoginProxy):
        if not LoginProxy.objectName():
            LoginProxy.setObjectName(u"LoginProxy")
        LoginProxy.resize(455, 418)
        self.gridLayout = QGridLayout(LoginProxy)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.testSpeedButton = QPushButton(LoginProxy)
        self.testSpeedButton.setObjectName(u"testSpeedButton")

        self.horizontalLayout_2.addWidget(self.testSpeedButton)

        self.label_2 = QLabel(LoginProxy)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_4 = QLabel(LoginProxy)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_4)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.radioButton_4 = QRadioButton(LoginProxy)
        self.buttonGroup = QButtonGroup(LoginProxy)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton_4)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.horizontalLayout_7.addWidget(self.radioButton_4)

        self.label7 = QLabel(LoginProxy)
        self.label7.setObjectName(u"label7")
        self.label7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label7)

        self.label8 = QLabel(LoginProxy)
        self.label8.setObjectName(u"label8")
        self.label8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label8)


        self.gridLayout.addLayout(self.horizontalLayout_7, 7, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton_3 = QRadioButton(LoginProxy)
        self.buttonGroup.addButton(self.radioButton_3)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.horizontalLayout_3.addWidget(self.radioButton_3)

        self.label5 = QLabel(LoginProxy)
        self.label5.setObjectName(u"label5")
        self.label5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label5)

        self.label6 = QLabel(LoginProxy)
        self.label6.setObjectName(u"label6")
        self.label6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label6)


        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radioButton_2 = QRadioButton(LoginProxy)
        self.buttonGroup.addButton(self.radioButton_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_4.addWidget(self.radioButton_2)

        self.label3 = QLabel(LoginProxy)
        self.label3.setObjectName(u"label3")
        self.label3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label3)

        self.label4 = QLabel(LoginProxy)
        self.label4.setObjectName(u"label4")
        self.label4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label4)


        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.radioButton_1 = QRadioButton(LoginProxy)
        self.buttonGroup.addButton(self.radioButton_1)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setChecked(True)

        self.horizontalLayout_5.addWidget(self.radioButton_1)

        self.label1 = QLabel(LoginProxy)
        self.label1.setObjectName(u"label1")
        self.label1.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label1)

        self.label2 = QLabel(LoginProxy)
        self.label2.setObjectName(u"label2")
        self.label2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label2)


        self.gridLayout.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_11 = QLabel(LoginProxy)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.label_11)

        self.cdnIp = QLineEdit(LoginProxy)
        self.cdnIp.setObjectName(u"cdnIp")

        self.horizontalLayout_6.addWidget(self.cdnIp)

        self.toolButton = QToolButton(LoginProxy)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout_6.addWidget(self.toolButton)


        self.gridLayout.addLayout(self.horizontalLayout_6, 6, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.saveButton = QPushButton(LoginProxy)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_8.addWidget(self.saveButton)


        self.gridLayout.addLayout(self.horizontalLayout_8, 8, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.proxyBox = QCheckBox(LoginProxy)
        self.proxyBox.setObjectName(u"proxyBox")

        self.horizontalLayout.addWidget(self.proxyBox)

        self.line = QFrame(LoginProxy)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label = QLabel(LoginProxy)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.httpLine = QLineEdit(LoginProxy)
        self.httpLine.setObjectName(u"httpLine")

        self.horizontalLayout.addWidget(self.httpLine)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.httpsBox = QCheckBox(LoginProxy)
        self.httpsBox.setObjectName(u"httpsBox")
        self.httpsBox.setChecked(True)

        self.horizontalLayout_9.addWidget(self.httpsBox)


        self.gridLayout.addLayout(self.horizontalLayout_9, 1, 0, 1, 1)


        self.retranslateUi(LoginProxy)
        self.testSpeedButton.clicked.connect(LoginProxy.SpeedTest)
        self.saveButton.clicked.connect(LoginProxy.SaveSetting)
        self.toolButton.clicked.connect(LoginProxy.OpenUrl)

        QMetaObject.connectSlotsByName(LoginProxy)
    # setupUi

    def retranslateUi(self, LoginProxy):
        LoginProxy.setWindowTitle(QCoreApplication.translate("LoginProxy", u"\u4ee3\u7406\u8bbe\u7f6e", None))
        self.testSpeedButton.setText(QCoreApplication.translate("LoginProxy", u"\u6d4b\u901f", None))
        self.label_2.setText(QCoreApplication.translate("LoginProxy", u"\u76f4\u8fde", None))
        self.label_4.setText(QCoreApplication.translate("LoginProxy", u"\u4ee3\u7406", None))
        self.radioButton_4.setText(QCoreApplication.translate("LoginProxy", u"CDN\u5206\u6d41", None))
        self.label7.setText("")
        self.label8.setText("")
        self.radioButton_3.setText(QCoreApplication.translate("LoginProxy", u"\u5206\u6d413", None))
        self.label5.setText("")
        self.label6.setText("")
        self.radioButton_2.setText(QCoreApplication.translate("LoginProxy", u"\u5206\u6d412", None))
        self.label3.setText("")
        self.label4.setText("")
        self.radioButton_1.setText(QCoreApplication.translate("LoginProxy", u"\u5206\u6d411", None))
        self.label1.setText("")
        self.label2.setText("")
        self.label_11.setText(QCoreApplication.translate("LoginProxy", u" CDN\u7684IP\u5730\u5740 ", None))
#if QT_CONFIG(tooltip)
        self.toolButton.setToolTip(QCoreApplication.translate("LoginProxy", u"<html><head/><body><p>\u81ea\u5b9a\u4e49host\uff0c\u586b\u5199<span style=\" font-family:'Consolas'; font-size:10.5pt; font-style:italic; color:#59626f;\">CloudFlare\u7684Ip\u5730\u5740</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton.setText(QCoreApplication.translate("LoginProxy", u"\uff1f", None))
        self.saveButton.setText(QCoreApplication.translate("LoginProxy", u"\u4fdd\u5b58", None))
        self.proxyBox.setText(QCoreApplication.translate("LoginProxy", u"\u542f\u7528\u4ee3\u7406", None))
        self.label.setText(QCoreApplication.translate("LoginProxy", u"\u4ee3\u7406\u5730\u5740", None))
        self.httpsBox.setText(QCoreApplication.translate("LoginProxy", u"\u542f\u7528HTTPS", None))
    # retranslateUi

