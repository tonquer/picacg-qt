# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_waifu2x_tool.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
    QFrame, QGraphicsView, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_Waifu2xTool(object):
    def setupUi(self, Waifu2xTool):
        if not Waifu2xTool.objectName():
            Waifu2xTool.setObjectName(u"Waifu2xTool")
        Waifu2xTool.resize(705, 498)
        self.gridLayout = QGridLayout(Waifu2xTool)
        self.gridLayout.setObjectName(u"gridLayout")
        self.graphicsView = QGraphicsView(Waifu2xTool)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = SmoothScrollArea(Waifu2xTool)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMaximumSize(QSize(300, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 281, 480))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.line_5 = QFrame(self.scrollAreaWidgetContents)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_5)

        self.checkBox = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMaximumSize(QSize(100, 16777215))
        self.checkBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox)

        self.ttaModel = QCheckBox(self.scrollAreaWidgetContents)
        self.ttaModel.setObjectName(u"ttaModel")
        self.ttaModel.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_2.addWidget(self.ttaModel, 0, Qt.AlignLeft)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.scaleRadio = QRadioButton(self.scrollAreaWidgetContents)
        self.buttonGroup_2 = QButtonGroup(Waifu2xTool)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.scaleRadio)
        self.scaleRadio.setObjectName(u"scaleRadio")
        self.scaleRadio.setMaximumSize(QSize(100, 16777215))
        self.scaleRadio.setChecked(True)

        self.horizontalLayout_3.addWidget(self.scaleRadio, 0, Qt.AlignLeft)

        self.scaleEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.scaleEdit.setObjectName(u"scaleEdit")
        self.scaleEdit.setMaximumSize(QSize(160, 16777215))
        self.scaleEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.scaleEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.heighRadio = QRadioButton(self.scrollAreaWidgetContents)
        self.buttonGroup_2.addButton(self.heighRadio)
        self.heighRadio.setObjectName(u"heighRadio")
        self.heighRadio.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_4.addWidget(self.heighRadio)

        self.widthEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.widthEdit.setObjectName(u"widthEdit")
        self.widthEdit.setEnabled(False)
        self.widthEdit.setMaximumSize(QSize(60, 16777215))
        self.widthEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.widthEdit)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(20, 16777215))

        self.horizontalLayout_4.addWidget(self.label_2)

        self.heighEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.heighEdit.setObjectName(u"heighEdit")
        self.heighEdit.setEnabled(False)
        self.heighEdit.setMaximumSize(QSize(60, 16777215))
        self.heighEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.heighEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_6.addWidget(self.label_5)

        self.modelName = QPushButton(self.scrollAreaWidgetContents)
        self.modelName.setObjectName(u"modelName")
        font = QFont()
        font.setPointSize(8)
        self.modelName.setFont(font)

        self.horizontalLayout_6.addWidget(self.modelName)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_7.addWidget(self.label_3)

        self.fmtComboBox = QComboBox(self.scrollAreaWidgetContents)
        self.fmtComboBox.addItem("")
        self.fmtComboBox.addItem("")
        self.fmtComboBox.addItem("")
        self.fmtComboBox.addItem("")
        self.fmtComboBox.addItem("")
        self.fmtComboBox.setObjectName(u"fmtComboBox")

        self.horizontalLayout_7.addWidget(self.fmtComboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.changeButton = QPushButton(self.scrollAreaWidgetContents)
        self.changeButton.setObjectName(u"changeButton")
        self.changeButton.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_2.addWidget(self.changeButton, 0, Qt.AlignHCenter)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_8.addWidget(self.label_8)

        self.resolutionLabel = QLabel(self.scrollAreaWidgetContents)
        self.resolutionLabel.setObjectName(u"resolutionLabel")
        self.resolutionLabel.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_8.addWidget(self.resolutionLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_9.addWidget(self.label_10)

        self.sizeLabel = QLabel(self.scrollAreaWidgetContents)
        self.sizeLabel.setObjectName(u"sizeLabel")
        self.sizeLabel.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_9.addWidget(self.sizeLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_11.addWidget(self.label_9, 0, Qt.AlignLeft)

        self.gpuLabel = QLabel(self.scrollAreaWidgetContents)
        self.gpuLabel.setObjectName(u"gpuLabel")
        self.gpuLabel.setMaximumSize(QSize(150, 16777215))
        self.gpuLabel.setWordWrap(True)

        self.horizontalLayout_11.addWidget(self.gpuLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.format = QLabel(self.scrollAreaWidgetContents)
        self.format.setObjectName(u"format")

        self.horizontalLayout.addWidget(self.format)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_10.addWidget(self.label_6, 0, Qt.AlignLeft)

        self.tickLabel = QLabel(self.scrollAreaWidgetContents)
        self.tickLabel.setObjectName(u"tickLabel")
        self.tickLabel.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_10.addWidget(self.tickLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.oepnButton = QPushButton(self.scrollAreaWidgetContents)
        self.oepnButton.setObjectName(u"oepnButton")
        self.oepnButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.oepnButton)

        self.saveButton = QPushButton(self.scrollAreaWidgetContents)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.saveButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_5.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_5.addWidget(self.pushButton_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.headButton = QPushButton(self.scrollAreaWidgetContents)
        self.headButton.setObjectName(u"headButton")
        self.headButton.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.headButton, 0, Qt.AlignHCenter)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)


        self.retranslateUi(Waifu2xTool)
        self.checkBox.clicked.connect(Waifu2xTool.SwithPicture)
        self.saveButton.clicked.connect(Waifu2xTool.SavePicture)
        self.heighEdit.textChanged.connect(Waifu2xTool.CheckScaleRadio)
        self.pushButton_3.clicked.connect(Waifu2xTool.ReduceScalePic)
        self.heighRadio.clicked.connect(Waifu2xTool.CheckScaleRadio)
        self.ttaModel.clicked.connect(Waifu2xTool.CheckScaleRadio)
        self.oepnButton.clicked.connect(Waifu2xTool.OpenPicture)
        self.widthEdit.textChanged.connect(Waifu2xTool.CheckScaleRadio)
        self.pushButton.clicked.connect(Waifu2xTool.AddScalePic)
        self.scaleEdit.textChanged.connect(Waifu2xTool.CheckScaleRadio)
        self.scaleRadio.clicked.connect(Waifu2xTool.CheckScaleRadio)
        self.changeButton.clicked.connect(Waifu2xTool.StartWaifu2x)
        self.headButton.clicked.connect(Waifu2xTool.SetHead)

        QMetaObject.connectSlotsByName(Waifu2xTool)
    # setupUi

    def retranslateUi(self, Waifu2xTool):
        Waifu2xTool.setWindowTitle(QCoreApplication.translate("Waifu2xTool", u"\u56fe\u7247\u67e5\u770b", None))
        self.checkBox.setText(QCoreApplication.translate("Waifu2xTool", u"waifu2x", None))
#if QT_CONFIG(tooltip)
        self.ttaModel.setToolTip(QCoreApplication.translate("Waifu2xTool", u"\u753b\u8d28\u63d0\u5347\uff0c\u8017\u65f6\u589e\u52a0", None))
#endif // QT_CONFIG(tooltip)
        self.ttaModel.setText(QCoreApplication.translate("Waifu2xTool", u"tta\u6a21\u5f0f", None))
        self.scaleRadio.setText(QCoreApplication.translate("Waifu2xTool", u"\u500d\u6570\u653e\u5927", None))
        self.scaleEdit.setText(QCoreApplication.translate("Waifu2xTool", u"2", None))
        self.heighRadio.setText(QCoreApplication.translate("Waifu2xTool", u"\u56fa\u5b9a\u957f\u5bbd", None))
        self.label_2.setText(QCoreApplication.translate("Waifu2xTool", u"X", None))
        self.label_5.setText(QCoreApplication.translate("Waifu2xTool", u"\u6a21\u578b\uff1a", None))
        self.modelName.setText("")
        self.label_3.setText(QCoreApplication.translate("Waifu2xTool", u"\u683c\u5f0f\uff1a", None))
        self.fmtComboBox.setItemText(0, QCoreApplication.translate("Waifu2xTool", u"\u81ea\u52a8", None))
        self.fmtComboBox.setItemText(1, QCoreApplication.translate("Waifu2xTool", u"JPG", None))
        self.fmtComboBox.setItemText(2, QCoreApplication.translate("Waifu2xTool", u"PNG", None))
        self.fmtComboBox.setItemText(3, QCoreApplication.translate("Waifu2xTool", u"BMP", None))
        self.fmtComboBox.setItemText(4, QCoreApplication.translate("Waifu2xTool", u"WEBP", None))

        self.changeButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u8f6c\u6362", None))
        self.label_8.setText(QCoreApplication.translate("Waifu2xTool", u"\u5206\u8fa8\u7387\uff1a", None))
        self.resolutionLabel.setText(QCoreApplication.translate("Waifu2xTool", u"\u65e0\u4fe1\u606f", None))
        self.label_10.setText(QCoreApplication.translate("Waifu2xTool", u"\u5927 \u5c0f\uff1a", None))
        self.sizeLabel.setText(QCoreApplication.translate("Waifu2xTool", u"\u65e0\u4fe1\u606f", None))
        self.label_9.setText(QCoreApplication.translate("Waifu2xTool", u"\u8f6c\u6362\u6a21\u5f0f\uff1a", None))
        self.gpuLabel.setText(QCoreApplication.translate("Waifu2xTool", u"GPU", None))
        self.label.setText(QCoreApplication.translate("Waifu2xTool", u"\u683c\u5f0f", None))
        self.format.setText("")
        self.label_6.setText(QCoreApplication.translate("Waifu2xTool", u"\u8017\u65f6\uff1a", None))
        self.tickLabel.setText("")
        self.oepnButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u6253\u5f00\u56fe\u7247", None))
        self.saveButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u4fdd\u5b58\u56fe\u7247", None))
        self.pushButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u653e\u5927", None))
        self.pushButton_3.setText(QCoreApplication.translate("Waifu2xTool", u"\u7f29\u5c0f", None))
        self.headButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u8bbe\u7f6e\u4e3a\u5934\u50cf", None))
    # retranslateUi

