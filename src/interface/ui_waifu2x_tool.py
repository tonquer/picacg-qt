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

class Ui_Waifu2xTool(object):
    def setupUi(self, Waifu2xTool):
        if not Waifu2xTool.objectName():
            Waifu2xTool.setObjectName(u"Waifu2xTool")
        Waifu2xTool.resize(502, 556)
        self.gridLayout = QGridLayout(Waifu2xTool)
        self.gridLayout.setObjectName(u"gridLayout")
        self.graphicsView = QGraphicsView(Waifu2xTool)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.line_3 = QFrame(Waifu2xTool)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.line_5 = QFrame(Waifu2xTool)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_5)

        self.checkBox = QCheckBox(Waifu2xTool)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMaximumSize(QSize(100, 16777215))
        self.checkBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox)

        self.ttaModel = QCheckBox(Waifu2xTool)
        self.ttaModel.setObjectName(u"ttaModel")
        self.ttaModel.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_2.addWidget(self.ttaModel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.scaleRadio = QRadioButton(Waifu2xTool)
        self.buttonGroup_2 = QButtonGroup(Waifu2xTool)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.scaleRadio)
        self.scaleRadio.setObjectName(u"scaleRadio")
        self.scaleRadio.setMaximumSize(QSize(100, 16777215))
        self.scaleRadio.setChecked(True)

        self.horizontalLayout_3.addWidget(self.scaleRadio)

        self.scaleEdit = QLineEdit(Waifu2xTool)
        self.scaleEdit.setObjectName(u"scaleEdit")
        self.scaleEdit.setMaximumSize(QSize(160, 16777215))
        self.scaleEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.scaleEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.heighRadio = QRadioButton(Waifu2xTool)
        self.buttonGroup_2.addButton(self.heighRadio)
        self.heighRadio.setObjectName(u"heighRadio")
        self.heighRadio.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_4.addWidget(self.heighRadio)

        self.widthEdit = QLineEdit(Waifu2xTool)
        self.widthEdit.setObjectName(u"widthEdit")
        self.widthEdit.setEnabled(False)
        self.widthEdit.setMaximumSize(QSize(60, 16777215))
        self.widthEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.widthEdit)

        self.label_2 = QLabel(Waifu2xTool)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(20, 16777215))

        self.horizontalLayout_4.addWidget(self.label_2)

        self.heighEdit = QLineEdit(Waifu2xTool)
        self.heighEdit.setObjectName(u"heighEdit")
        self.heighEdit.setEnabled(False)
        self.heighEdit.setMaximumSize(QSize(60, 16777215))
        self.heighEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.heighEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(Waifu2xTool)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_5.addWidget(self.label_4)

        self.noiseCombox = QComboBox(Waifu2xTool)
        self.noiseCombox.addItem("")
        self.noiseCombox.addItem("")
        self.noiseCombox.addItem("")
        self.noiseCombox.addItem("")
        self.noiseCombox.addItem("")
        self.noiseCombox.setObjectName(u"noiseCombox")
        self.noiseCombox.setMinimumSize(QSize(160, 0))
        self.noiseCombox.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_5.addWidget(self.noiseCombox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(Waifu2xTool)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_6.addWidget(self.label_5)

        self.comboBox = QComboBox(Waifu2xTool)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(160, 0))
        self.comboBox.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_6.addWidget(self.comboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")

        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.changeButton = QPushButton(Waifu2xTool)
        self.changeButton.setObjectName(u"changeButton")
        self.changeButton.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_2.addWidget(self.changeButton, 0, Qt.AlignLeft)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.line = QFrame(Waifu2xTool)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.line_4 = QFrame(Waifu2xTool)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_8 = QLabel(Waifu2xTool)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_8.addWidget(self.label_8)

        self.resolutionLabel = QLabel(Waifu2xTool)
        self.resolutionLabel.setObjectName(u"resolutionLabel")
        self.resolutionLabel.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_8.addWidget(self.resolutionLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_10 = QLabel(Waifu2xTool)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_9.addWidget(self.label_10)

        self.sizeLabel = QLabel(Waifu2xTool)
        self.sizeLabel.setObjectName(u"sizeLabel")
        self.sizeLabel.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_9.addWidget(self.sizeLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_9 = QLabel(Waifu2xTool)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_11.addWidget(self.label_9)

        self.gpuLabel = QLabel(Waifu2xTool)
        self.gpuLabel.setObjectName(u"gpuLabel")
        self.gpuLabel.setWordWrap(True)

        self.horizontalLayout_11.addWidget(self.gpuLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Waifu2xTool)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.format = QLabel(Waifu2xTool)
        self.format.setObjectName(u"format")

        self.horizontalLayout.addWidget(self.format)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_6 = QLabel(Waifu2xTool)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_10.addWidget(self.label_6)

        self.tickLabel = QLabel(Waifu2xTool)
        self.tickLabel.setObjectName(u"tickLabel")
        self.tickLabel.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_10.addWidget(self.tickLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.oepnButton = QPushButton(Waifu2xTool)
        self.oepnButton.setObjectName(u"oepnButton")
        self.oepnButton.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.oepnButton, 0, Qt.AlignLeft)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.pushButton_3 = QPushButton(Waifu2xTool)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.pushButton_3, 0, Qt.AlignLeft)

        self.pushButton = QPushButton(Waifu2xTool)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.pushButton, 0, Qt.AlignLeft)

        self.saveButton = QPushButton(Waifu2xTool)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.saveButton, 0, Qt.AlignLeft)

        self.headButton = QPushButton(Waifu2xTool)
        self.headButton.setObjectName(u"headButton")
        self.headButton.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.headButton, 0, Qt.AlignLeft)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.line_6 = QFrame(Waifu2xTool)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.line_2 = QFrame(Waifu2xTool)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)


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
        self.comboBox.currentIndexChanged.connect(Waifu2xTool.ChangeModel)
        self.changeButton.clicked.connect(Waifu2xTool.StartWaifu2x)
        self.noiseCombox.currentIndexChanged.connect(Waifu2xTool.CheckScaleRadio)
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
        self.label_4.setText(QCoreApplication.translate("Waifu2xTool", u"\u964d\u566a\uff1a", None))
        self.noiseCombox.setItemText(0, QCoreApplication.translate("Waifu2xTool", u"3", None))
        self.noiseCombox.setItemText(1, QCoreApplication.translate("Waifu2xTool", u"2", None))
        self.noiseCombox.setItemText(2, QCoreApplication.translate("Waifu2xTool", u"1", None))
        self.noiseCombox.setItemText(3, QCoreApplication.translate("Waifu2xTool", u"0", None))
        self.noiseCombox.setItemText(4, QCoreApplication.translate("Waifu2xTool", u"-1", None))

        self.label_5.setText(QCoreApplication.translate("Waifu2xTool", u"\u6a21\u578b\uff1a", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Waifu2xTool", u"cunet", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Waifu2xTool", u"photo", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Waifu2xTool", u"anime_style_art_rgb", None))

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
        self.pushButton_3.setText(QCoreApplication.translate("Waifu2xTool", u"\u7f29\u5c0f", None))
        self.pushButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u653e\u5927", None))
        self.saveButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u4fdd\u5b58\u56fe\u7247", None))
        self.headButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u8bbe\u7f6e\u5934\u50cf", None))
    # retranslateUi

