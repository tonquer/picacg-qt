# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_login_proxy_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QCommandLinkButton,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from component.box.wheel_combo_box import WheelComboBox
from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_LoginProxyWidget(object):
    def setupUi(self, LoginProxyWidget):
        if not LoginProxyWidget.objectName():
            LoginProxyWidget.setObjectName(u"LoginProxyWidget")
        LoginProxyWidget.resize(577, 473)
        LoginProxyWidget.setMinimumSize(QSize(550, 0))
        self.gridLayout = QGridLayout(LoginProxyWidget)
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName(u"gridLayout")
        self.scrollArea = SmoothScrollArea(LoginProxyWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 540, 541))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.proxy_0 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup = QButtonGroup(LoginProxyWidget)
        self.radioProxyGroup.setObjectName(u"radioProxyGroup")
        self.radioProxyGroup.addButton(self.proxy_0)
        self.proxy_0.setObjectName(u"proxy_0")

        self.horizontalLayout_11.addWidget(self.proxy_0)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.proxy_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup.addButton(self.proxy_1)
        self.proxy_1.setObjectName(u"proxy_1")
        self.proxy_1.setMinimumSize(QSize(90, 0))

        self.horizontalLayout.addWidget(self.proxy_1)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.httpLine = QLineEdit(self.scrollAreaWidgetContents)
        self.httpLine.setObjectName(u"httpLine")

        self.horizontalLayout.addWidget(self.httpLine)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.proxy_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup.addButton(self.proxy_2)
        self.proxy_2.setObjectName(u"proxy_2")
        self.proxy_2.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_10.addWidget(self.proxy_2)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_10.addWidget(self.line_2)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_10.addWidget(self.label_5)

        self.sockEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.sockEdit.setObjectName(u"sockEdit")

        self.horizontalLayout_10.addWidget(self.sockEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.proxy_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup.addButton(self.proxy_3)
        self.proxy_3.setObjectName(u"proxy_3")

        self.horizontalLayout_12.addWidget(self.proxy_3)

        self.checkLabel = QLabel(self.scrollAreaWidgetContents)
        self.checkLabel.setObjectName(u"checkLabel")
        font = QFont()
        font.setBold(False)
        self.checkLabel.setFont(font)
        self.checkLabel.setStyleSheet(u"color:rgb(255, 0, 0)")

        self.horizontalLayout_12.addWidget(self.checkLabel)

        self.proxyLabel = QLabel(self.scrollAreaWidgetContents)
        self.proxyLabel.setObjectName(u"proxyLabel")

        self.horizontalLayout_12.addWidget(self.proxyLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.line_3 = QFrame(self.scrollAreaWidgetContents)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_12 = QLabel(self.scrollAreaWidgetContents)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_4.addWidget(self.label_12)

        self.apiTimeout = WheelComboBox(self.scrollAreaWidgetContents)
        self.apiTimeout.addItem("")
        self.apiTimeout.addItem("")
        self.apiTimeout.addItem("")
        self.apiTimeout.setObjectName(u"apiTimeout")

        self.horizontalLayout_4.addWidget(self.apiTimeout)

        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_4.addWidget(self.label_10)

        self.imgTimeout = WheelComboBox(self.scrollAreaWidgetContents)
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.setObjectName(u"imgTimeout")

        self.horizontalLayout_4.addWidget(self.imgTimeout)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ipv6Check = QCheckBox(self.scrollAreaWidgetContents)
        self.ipv6Check.setObjectName(u"ipv6Check")

        self.horizontalLayout_2.addWidget(self.ipv6Check)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.httpsBox = QCheckBox(self.scrollAreaWidgetContents)
        self.httpsBox.setObjectName(u"httpsBox")
        self.httpsBox.setChecked(True)

        self.horizontalLayout_9.addWidget(self.httpsBox)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_3.addWidget(self.label_9)

        self.imgCombox = WheelComboBox(self.scrollAreaWidgetContents)
        self.imgCombox.setObjectName(u"imgCombox")

        self.horizontalLayout_3.addWidget(self.imgCombox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.testSpeedButton = QPushButton(self.scrollAreaWidgetContents)
        self.testSpeedButton.setObjectName(u"testSpeedButton")

        self.verticalLayout.addWidget(self.testSpeedButton)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_img_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_5.setObjectName(u"label_img_5")

        self.gridLayout_2.addWidget(self.label_img_5, 5, 3, 1, 1)

        self.radioButton_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup = QButtonGroup(LoginProxyWidget)
        self.radioApiGroup.setObjectName(u"radioApiGroup")
        self.radioApiGroup.addButton(self.radioButton_3)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.gridLayout_2.addWidget(self.radioButton_3, 4, 0, 1, 1)

        self.radioButton_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup.addButton(self.radioButton_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_2.addWidget(self.radioButton_2, 3, 0, 1, 1)

        self.cdn_img_ip = QLineEdit(self.scrollAreaWidgetContents)
        self.cdn_img_ip.setObjectName(u"cdn_img_ip")
        self.cdn_img_ip.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_2.addWidget(self.cdn_img_ip, 8, 3, 1, 1)

        self.radio_img_6 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup = QButtonGroup(LoginProxyWidget)
        self.radioImgGroup.setObjectName(u"radioImgGroup")
        self.radioImgGroup.addButton(self.radio_img_6)
        self.radio_img_6.setObjectName(u"radio_img_6")

        self.gridLayout_2.addWidget(self.radio_img_6, 6, 2, 1, 1)

        self.radioButton_6 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup.addButton(self.radioButton_6)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.gridLayout_2.addWidget(self.radioButton_6, 6, 0, 1, 1)

        self.radio_img_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup.addButton(self.radio_img_3)
        self.radio_img_3.setObjectName(u"radio_img_3")

        self.gridLayout_2.addWidget(self.radio_img_3, 4, 2, 1, 1)

        self.label_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_11, 8, 0, 1, 1)

        self.radioButton_4 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup.addButton(self.radioButton_4)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.gridLayout_2.addWidget(self.radioButton_4, 7, 0, 1, 1)

        self.label_img_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_6.setObjectName(u"label_img_6")

        self.gridLayout_2.addWidget(self.label_img_6, 6, 3, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 8, 2, 1, 1)

        self.cdn_api_ip = QLineEdit(self.scrollAreaWidgetContents)
        self.cdn_api_ip.setObjectName(u"cdn_api_ip")
        self.cdn_api_ip.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_2.addWidget(self.cdn_api_ip, 8, 1, 1, 1)

        self.label_api_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_3.setObjectName(u"label_api_3")

        self.gridLayout_2.addWidget(self.label_api_3, 4, 1, 1, 1)

        self.label_api_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_2.setObjectName(u"label_api_2")

        self.gridLayout_2.addWidget(self.label_api_2, 3, 1, 1, 1)

        self.label_img_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_3.setObjectName(u"label_img_3")

        self.gridLayout_2.addWidget(self.label_img_3, 4, 3, 1, 1)

        self.label_img_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_1.setObjectName(u"label_img_1")

        self.gridLayout_2.addWidget(self.label_img_1, 2, 3, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_7, 1, 2, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_6, 1, 1, 1, 1)

        self.radio_img_5 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup.addButton(self.radio_img_5)
        self.radio_img_5.setObjectName(u"radio_img_5")

        self.gridLayout_2.addWidget(self.radio_img_5, 5, 2, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_4, 1, 3, 1, 1)

        self.radioButton_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup.addButton(self.radioButton_1)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_1, 2, 0, 1, 1)

        self.radio_img_4 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup.addButton(self.radio_img_4)
        self.radio_img_4.setObjectName(u"radio_img_4")

        self.gridLayout_2.addWidget(self.radio_img_4, 7, 2, 1, 1)

        self.label_api_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_5.setObjectName(u"label_api_5")

        self.gridLayout_2.addWidget(self.label_api_5, 5, 1, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_img_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_4.setObjectName(u"label_img_4")

        self.gridLayout_2.addWidget(self.label_img_4, 7, 3, 1, 1)

        self.label_api_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_6.setObjectName(u"label_api_6")

        self.gridLayout_2.addWidget(self.label_api_6, 6, 1, 1, 1)

        self.label_img_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_2.setObjectName(u"label_img_2")

        self.gridLayout_2.addWidget(self.label_img_2, 3, 3, 1, 1)

        self.radio_img_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup.addButton(self.radio_img_1)
        self.radio_img_1.setObjectName(u"radio_img_1")
        self.radio_img_1.setChecked(True)

        self.gridLayout_2.addWidget(self.radio_img_1, 2, 2, 1, 1)

        self.label_api_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_4.setObjectName(u"label_api_4")

        self.gridLayout_2.addWidget(self.label_api_4, 7, 1, 1, 1)

        self.label_api_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_1.setObjectName(u"label_api_1")

        self.gridLayout_2.addWidget(self.label_api_1, 2, 1, 1, 1)

        self.radio_img_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup.addButton(self.radio_img_2)
        self.radio_img_2.setObjectName(u"radio_img_2")

        self.gridLayout_2.addWidget(self.radio_img_2, 3, 2, 1, 1)

        self.radioButton_5 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup.addButton(self.radioButton_5)
        self.radioButton_5.setObjectName(u"radioButton_5")

        self.gridLayout_2.addWidget(self.radioButton_5, 5, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_8.addWidget(self.label_3)

        self.commandLinkButton = QCommandLinkButton(self.scrollAreaWidgetContents)
        self.commandLinkButton.setObjectName(u"commandLinkButton")

        self.horizontalLayout_8.addWidget(self.commandLinkButton)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(LoginProxyWidget)
        self.testSpeedButton.clicked.connect(LoginProxyWidget.SpeedTest)

        QMetaObject.connectSlotsByName(LoginProxyWidget)
    # setupUi

    def retranslateUi(self, LoginProxyWidget):
        LoginProxyWidget.setWindowTitle(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406\u8bbe\u7f6e", None))
        self.proxy_0.setText(QCoreApplication.translate("LoginProxyWidget", u"\u65e0\u4ee3\u7406", None))
        self.proxy_1.setText(QCoreApplication.translate("LoginProxyWidget", u"HTTP\u4ee3\u7406", None))
        self.label.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406\u5730\u5740", None))
#if QT_CONFIG(tooltip)
        self.httpLine.setToolTip(QCoreApplication.translate("LoginProxyWidget", u"http://127.0.0.1:10809", None))
#endif // QT_CONFIG(tooltip)
        self.httpLine.setPlaceholderText("")
        self.proxy_2.setText(QCoreApplication.translate("LoginProxyWidget", u"Sock5\u4ee3\u7406", None))
        self.label_5.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406\u5730\u5740", None))
#if QT_CONFIG(tooltip)
        self.sockEdit.setToolTip(QCoreApplication.translate("LoginProxyWidget", u"127.0.0.1:10808", None))
#endif // QT_CONFIG(tooltip)
        self.sockEdit.setPlaceholderText("")
        self.proxy_3.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4f7f\u7528\u7cfb\u7edf\u4ee3\u7406", None))
        self.checkLabel.setText(QCoreApplication.translate("LoginProxyWidget", u"\u672a\u68c0\u6d4b\u5230\u7cfb\u7edf\u4ee3\u7406", None))
        self.proxyLabel.setText("")
        self.label_12.setText(QCoreApplication.translate("LoginProxyWidget", u"API\u8d85\u65f6\u65f6\u95f4  ", None))
        self.apiTimeout.setItemText(0, QCoreApplication.translate("LoginProxyWidget", u"2", None))
        self.apiTimeout.setItemText(1, QCoreApplication.translate("LoginProxyWidget", u"5", None))
        self.apiTimeout.setItemText(2, QCoreApplication.translate("LoginProxyWidget", u"7", None))

        self.label_10.setText(QCoreApplication.translate("LoginProxyWidget", u"\u56fe\u7247\u8d85\u65f6\u65f6\u95f4 ", None))
        self.imgTimeout.setItemText(0, QCoreApplication.translate("LoginProxyWidget", u"2", None))
        self.imgTimeout.setItemText(1, QCoreApplication.translate("LoginProxyWidget", u"5", None))
        self.imgTimeout.setItemText(2, QCoreApplication.translate("LoginProxyWidget", u"7", None))
        self.imgTimeout.setItemText(3, QCoreApplication.translate("LoginProxyWidget", u"10", None))
        self.imgTimeout.setItemText(4, QCoreApplication.translate("LoginProxyWidget", u"15", None))

        self.ipv6Check.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4f18\u5148\u4f7f\u7528IPV6\u5206\u6d41\uff08\u5206\u6d412\u30013\u652f\u6301\uff09", None))
        self.httpsBox.setText(QCoreApplication.translate("LoginProxyWidget", u"\u542f\u7528Https\uff08\u5982\u679c\u51fa\u73b0\u8fde\u63a5\u88ab\u91cd\u7f6e\uff0c\u5efa\u8bae\u5173\u95ed\u8bd5\u8bd5\uff09", None))
        self.label_9.setText(QCoreApplication.translate("LoginProxyWidget", u"\u56fe\u7247\u5730\u5740\u9009\u62e9\uff1a", None))
        self.testSpeedButton.setText(QCoreApplication.translate("LoginProxyWidget", u"\u6d4b\u901f", None))
        self.label_img_5.setText("")
        self.radioButton_3.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d413", None))
        self.radioButton_2.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d412", None))
        self.radio_img_6.setText(QCoreApplication.translate("LoginProxyWidget", u"US\u53cd\u4ee3\u5206\u6d41", None))
        self.radioButton_6.setText(QCoreApplication.translate("LoginProxyWidget", u"US\u53cd\u4ee3\u5206\u6d41", None))
        self.radio_img_3.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d413", None))
        self.label_11.setText(QCoreApplication.translate("LoginProxyWidget", u" CDN\u5730\u5740 ", None))
        self.radioButton_4.setText(QCoreApplication.translate("LoginProxyWidget", u"CDN\u5206\u6d41", None))
        self.label_img_6.setText("")
        self.label_8.setText(QCoreApplication.translate("LoginProxyWidget", u"CDN\u5730\u5740", None))
        self.label_api_3.setText("")
        self.label_api_2.setText("")
        self.label_img_3.setText("")
        self.label_img_1.setText("")
        self.label_7.setText(QCoreApplication.translate("LoginProxyWidget", u"\u56fe\u7247\u5206\u6d41", None))
        self.label_6.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5ef6\u8fdf", None))
#if QT_CONFIG(tooltip)
        self.radio_img_5.setToolTip(QCoreApplication.translate("LoginProxyWidget", u"\u6240\u4ee5\u5206\u6d41\u4e0d\u53ef\u4f7f\u7528\u65f6\uff0c\u81ea\u52a8\u89e3\u9501", None))
#endif // QT_CONFIG(tooltip)
        self.radio_img_5.setText(QCoreApplication.translate("LoginProxyWidget", u"JP\u53cd\u4ee3\u5206\u6d41", None))
        self.label_4.setText(QCoreApplication.translate("LoginProxyWidget", u"\u901f\u5ea6", None))
        self.radioButton_1.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d411", None))
        self.radio_img_4.setText(QCoreApplication.translate("LoginProxyWidget", u"CDN\u5206\u6d41", None))
        self.label_api_5.setText("")
        self.label_2.setText(QCoreApplication.translate("LoginProxyWidget", u"Api\u5206\u6d41", None))
        self.label_img_4.setText("")
        self.label_api_6.setText("")
        self.label_img_2.setText("")
        self.radio_img_1.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d411", None))
        self.label_api_4.setText("")
        self.label_api_1.setText("")
        self.radio_img_2.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d412", None))
#if QT_CONFIG(tooltip)
        self.radioButton_5.setToolTip(QCoreApplication.translate("LoginProxyWidget", u"\u6240\u4ee5\u5206\u6d41\u4e0d\u53ef\u4f7f\u7528\u65f6\uff0c\u81ea\u52a8\u89e3\u9501", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_5.setText(QCoreApplication.translate("LoginProxyWidget", u"JP\u53cd\u4ee3\u5206\u6d41", None))
        self.label_3.setText(QCoreApplication.translate("LoginProxyWidget", u"CDN\u8bbe\u7f6e\u8bf7\u770b\u8bf4\u660e\u83b7\u53d6", None))
        self.commandLinkButton.setText(QCoreApplication.translate("LoginProxyWidget", u"\u8bf4\u660e", None))
    # retranslateUi

