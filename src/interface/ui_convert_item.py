# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_convert_item.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QToolButton, QVBoxLayout, QWidget)

from component.box.wheel_combo_box import WheelComboBox
from component.box.wheel_double_spin_box import WheelDoubleSpinBox
from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_ConvertItem(object):
    def setupUi(self, ConvertItem):
        if not ConvertItem.objectName():
            ConvertItem.setObjectName(u"ConvertItem")
        ConvertItem.resize(539, 546)
        self.verticalLayout_7 = QVBoxLayout(ConvertItem)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.scrollArea = SmoothScrollArea(ConvertItem)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 519, 494))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.convert_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.convertGroup = QButtonGroup(ConvertItem)
        self.convertGroup.setObjectName(u"convertGroup")
        self.convertGroup.addButton(self.convert_2)
        self.convert_2.setObjectName(u"convert_2")

        self.gridLayout_3.addWidget(self.convert_2, 1, 1, 1, 1)

        self.compose_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.composeGroup = QButtonGroup(ConvertItem)
        self.composeGroup.setObjectName(u"composeGroup")
        self.composeGroup.addButton(self.compose_1)
        self.compose_1.setObjectName(u"compose_1")
        self.compose_1.setChecked(True)

        self.gridLayout_3.addWidget(self.compose_1, 0, 0, 1, 1)

        self.convert_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.convertGroup.addButton(self.convert_1)
        self.convert_1.setObjectName(u"convert_1")
        self.convert_1.setChecked(True)

        self.gridLayout_3.addWidget(self.convert_1, 0, 1, 1, 1)

        self.compose_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.composeGroup.addButton(self.compose_2)
        self.compose_2.setObjectName(u"compose_2")

        self.gridLayout_3.addWidget(self.compose_2, 1, 0, 1, 1)

        self.convert_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.convertGroup.addButton(self.convert_3)
        self.convert_3.setObjectName(u"convert_3")

        self.gridLayout_3.addWidget(self.convert_3, 2, 1, 1, 1)

        self.convert_4 = QRadioButton(self.scrollAreaWidgetContents)
        self.convertGroup.addButton(self.convert_4)
        self.convert_4.setObjectName(u"convert_4")

        self.gridLayout_3.addWidget(self.convert_4, 3, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_3, 3, 1, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(60, 16777215))

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.importLine = QLineEdit(self.scrollAreaWidgetContents)
        self.importLine.setObjectName(u"importLine")

        self.horizontalLayout.addWidget(self.importLine)

        self.importButton = QToolButton(self.scrollAreaWidgetContents)
        self.importButton.setObjectName(u"importButton")

        self.horizontalLayout.addWidget(self.importButton)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(120, 0))

        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)

        self.checkBox = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMinimumSize(QSize(120, 0))
        self.checkBox.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 1, 1, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(60, 16777215))

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(60, 16777215))

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.coverCheckBox = QCheckBox(self.scrollAreaWidgetContents)
        self.coverCheckBox.setObjectName(u"coverCheckBox")
        self.coverCheckBox.setChecked(True)

        self.verticalLayout_4.addWidget(self.coverCheckBox)

        self.ttaCheck = QCheckBox(self.scrollAreaWidgetContents)
        self.ttaCheck.setObjectName(u"ttaCheck")

        self.verticalLayout_4.addWidget(self.ttaCheck)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_23 = QLabel(self.scrollAreaWidgetContents)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(60, 0))
        self.label_23.setMaximumSize(QSize(156, 16777215))

        self.horizontalLayout_12.addWidget(self.label_23)

        self.coverNoise = WheelComboBox(self.scrollAreaWidgetContents)
        self.coverNoise.addItem("")
        self.coverNoise.addItem("")
        self.coverNoise.addItem("")
        self.coverNoise.addItem("")
        self.coverNoise.setObjectName(u"coverNoise")
        self.coverNoise.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_12.addWidget(self.coverNoise)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_10)


        self.verticalLayout_4.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_26 = QLabel(self.scrollAreaWidgetContents)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(60, 0))
        self.label_26.setMaximumSize(QSize(156, 16777215))

        self.horizontalLayout_14.addWidget(self.label_26)

        self.coverModel_2 = WheelComboBox(self.scrollAreaWidgetContents)
        self.coverModel_2.addItem("")
        self.coverModel_2.addItem("")
        self.coverModel_2.addItem("")
        self.coverModel_2.setObjectName(u"coverModel_2")
        self.coverModel_2.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_14.addWidget(self.coverModel_2)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_12)


        self.verticalLayout_4.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.scale_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.scaleGroup = QButtonGroup(ConvertItem)
        self.scaleGroup.setObjectName(u"scaleGroup")
        self.scaleGroup.addButton(self.scale_1)
        self.scale_1.setObjectName(u"scale_1")
        self.scale_1.setMinimumSize(QSize(120, 0))
        self.scale_1.setChecked(True)

        self.horizontalLayout_15.addWidget(self.scale_1)

        self.coverScale = WheelDoubleSpinBox(self.scrollAreaWidgetContents)
        self.coverScale.setObjectName(u"coverScale")
        self.coverScale.setMinimumSize(QSize(150, 0))
        self.coverScale.setDecimals(1)
        self.coverScale.setMaximum(32.000000000000000)
        self.coverScale.setSingleStep(0.100000000000000)
        self.coverScale.setValue(2.000000000000000)

        self.horizontalLayout_15.addWidget(self.coverScale)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_13)


        self.verticalLayout_4.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.scale_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.scaleGroup.addButton(self.scale_2)
        self.scale_2.setObjectName(u"scale_2")
        self.scale_2.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_4.addWidget(self.scale_2)

        self.scale_x = QSpinBox(self.scrollAreaWidgetContents)
        self.scale_x.setObjectName(u"scale_x")
        self.scale_x.setMinimumSize(QSize(100, 0))
        self.scale_x.setMaximum(100000)
        self.scale_x.setValue(1920)

        self.horizontalLayout_4.addWidget(self.scale_x)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_4.addWidget(self.label_8)

        self.scale_y = QSpinBox(self.scrollAreaWidgetContents)
        self.scale_y.setObjectName(u"scale_y")
        self.scale_y.setMinimumSize(QSize(100, 0))
        self.scale_y.setMaximum(100000)
        self.scale_y.setValue(1080)

        self.horizontalLayout_4.addWidget(self.scale_y)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.gridLayout.addLayout(self.verticalLayout_4, 2, 1, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(60, 16777215))

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(120, 0))
        self.label_9.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_5.addWidget(self.label_9, 0, 0, 1, 1)

        self.cacheDir = QLabel(self.scrollAreaWidgetContents)
        self.cacheDir.setObjectName(u"cacheDir")

        self.gridLayout_5.addWidget(self.cacheDir, 0, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_5, 4, 1, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.exportLine = QLineEdit(self.scrollAreaWidgetContents)
        self.exportLine.setObjectName(u"exportLine")

        self.gridLayout_4.addWidget(self.exportLine, 0, 1, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(120, 0))

        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 1)

        self.exportButton = QToolButton(self.scrollAreaWidgetContents)
        self.exportButton.setObjectName(u"exportButton")

        self.gridLayout_4.addWidget(self.exportButton, 0, 2, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_4, 5, 1, 1, 1)


        self.verticalLayout_8.addLayout(self.gridLayout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_7.addWidget(self.scrollArea)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.loginButton = QPushButton(ConvertItem)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setMaximumSize(QSize(150, 30))
        self.loginButton.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.loginButton)

        self.closeButton = QPushButton(ConvertItem)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMaximumSize(QSize(150, 30))

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_3)


        self.retranslateUi(ConvertItem)

        self.coverNoise.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(ConvertItem)
    # setupUi

    def retranslateUi(self, ConvertItem):
        ConvertItem.setWindowTitle(QCoreApplication.translate("ConvertItem", u"\u8f6c\u6362\u9009\u9879", None))
        self.convert_2.setText(QCoreApplication.translate("ConvertItem", u"\u7edf\u4e00\u8f6c\u6362\u4e3aPNG", None))
        self.compose_1.setText(QCoreApplication.translate("ConvertItem", u"\u65e0", None))
        self.convert_1.setText(QCoreApplication.translate("ConvertItem", u"\u65e0", None))
        self.compose_2.setText(QCoreApplication.translate("ConvertItem", u"\u6253\u5305\u6210ZIP", None))
        self.convert_3.setText(QCoreApplication.translate("ConvertItem", u"\u7edf\u4e00\u8f6c\u6362\u4e3aJPG", None))
        self.convert_4.setText(QCoreApplication.translate("ConvertItem", u"\u7edf\u4e00\u8f6c\u6362\u4e3aWEBP", None))
        self.label_4.setText(QCoreApplication.translate("ConvertItem", u"\u8f93\u51fa\uff1a", None))
        self.importButton.setText(QCoreApplication.translate("ConvertItem", u"...", None))
        self.label_6.setText(QCoreApplication.translate("ConvertItem", u"\u8f93\u5165\u76ee\u5f55\uff1a", None))
        self.checkBox.setText(QCoreApplication.translate("ConvertItem", u"\u662f\u5426\u591a\u7ae0\u8282\u76ee\u5f55", None))
        self.label_2.setText(QCoreApplication.translate("ConvertItem", u"Waifu2x", None))
        self.label_3.setText(QCoreApplication.translate("ConvertItem", u"\u538b\u7f29\uff1a", None))
        self.coverCheckBox.setText(QCoreApplication.translate("ConvertItem", u"\u662f\u5426\u542f\u7528", None))
        self.ttaCheck.setText(QCoreApplication.translate("ConvertItem", u"TTA\u6a21\u5f0f\uff08\u9ad8\u8d28\u91cf\uff09", None))
        self.label_23.setText(QCoreApplication.translate("ConvertItem", u"\u53bb\u566a\u7b49\u7ea7", None))
        self.coverNoise.setItemText(0, QCoreApplication.translate("ConvertItem", u"0", None))
        self.coverNoise.setItemText(1, QCoreApplication.translate("ConvertItem", u"1", None))
        self.coverNoise.setItemText(2, QCoreApplication.translate("ConvertItem", u"2", None))
        self.coverNoise.setItemText(3, QCoreApplication.translate("ConvertItem", u"3", None))

        self.label_26.setText(QCoreApplication.translate("ConvertItem", u"\u6a21\u578b", None))
        self.coverModel_2.setItemText(0, QCoreApplication.translate("ConvertItem", u"cunet", None))
        self.coverModel_2.setItemText(1, QCoreApplication.translate("ConvertItem", u"photo", None))
        self.coverModel_2.setItemText(2, QCoreApplication.translate("ConvertItem", u"anime_style_art_rgb", None))

        self.scale_1.setText(QCoreApplication.translate("ConvertItem", u"\u4f7f\u7528\u653e\u5927\u500d\u7387", None))
        self.scale_2.setText(QCoreApplication.translate("ConvertItem", u"\u4f7f\u7528\u56fa\u5b9a\u5206\u8fa8\u7387", None))
        self.label_8.setText(QCoreApplication.translate("ConvertItem", u"x", None))
        self.label_5.setText(QCoreApplication.translate("ConvertItem", u"\u8f93\u5165\uff1a", None))
        self.label.setText(QCoreApplication.translate("ConvertItem", u"\u5176\u4ed6:", None))
        self.label_9.setText(QCoreApplication.translate("ConvertItem", u"\u7f13\u5b58\u76ee\u5f55\uff1a", None))
        self.cacheDir.setText("")
        self.label_7.setText(QCoreApplication.translate("ConvertItem", u"\u8f93\u51fa\u76ee\u5f55\uff1a", None))
        self.exportButton.setText(QCoreApplication.translate("ConvertItem", u"...", None))
        self.loginButton.setText(QCoreApplication.translate("ConvertItem", u"\u786e\u5b9a", None))
#if QT_CONFIG(shortcut)
        self.loginButton.setShortcut(QCoreApplication.translate("ConvertItem", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.closeButton.setText(QCoreApplication.translate("ConvertItem", u"\u5173\u95ed", None))
    # retranslateUi

