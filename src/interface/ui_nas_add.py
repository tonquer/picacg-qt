# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_nas_add.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_NasAdd(object):
    def setupUi(self, NasAdd):
        if not NasAdd.objectName():
            NasAdd.setObjectName(u"NasAdd")
        NasAdd.resize(897, 515)
        self.verticalLayout = QVBoxLayout(NasAdd)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBox = QComboBox(NasAdd)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_2.addWidget(self.comboBox, 0, 2, 1, 1)

        self.pathEdit = QLineEdit(NasAdd)
        self.pathEdit.setObjectName(u"pathEdit")

        self.gridLayout_2.addWidget(self.pathEdit, 5, 2, 1, 1)

        self.label_port = QLabel(NasAdd)
        self.label_port.setObjectName(u"label_port")
        self.label_port.setMinimumSize(QSize(80, 30))

        self.gridLayout_2.addWidget(self.label_port, 3, 0, 1, 1)

        self.label_address = QLabel(NasAdd)
        self.label_address.setObjectName(u"label_address")
        self.label_address.setMinimumSize(QSize(80, 30))

        self.gridLayout_2.addWidget(self.label_address, 2, 0, 1, 1)

        self.userEdit = QLineEdit(NasAdd)
        self.userEdit.setObjectName(u"userEdit")

        self.gridLayout_2.addWidget(self.userEdit, 6, 2, 1, 1)

        self.label_8 = QLabel(NasAdd)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(80, 30))

        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.compress1Radio = QRadioButton(NasAdd)
        self.compressGroup = QButtonGroup(NasAdd)
        self.compressGroup.setObjectName(u"compressGroup")
        self.compressGroup.addButton(self.compress1Radio)
        self.compress1Radio.setObjectName(u"compress1Radio")
        self.compress1Radio.setChecked(True)

        self.horizontalLayout.addWidget(self.compress1Radio)

        self.compress2Radio = QRadioButton(NasAdd)
        self.compressGroup.addButton(self.compress2Radio)
        self.compress2Radio.setObjectName(u"compress2Radio")

        self.horizontalLayout.addWidget(self.compress2Radio)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout, 8, 2, 1, 1)

        self.label_path = QLabel(NasAdd)
        self.label_path.setObjectName(u"label_path")
        self.label_path.setMinimumSize(QSize(80, 30))

        self.gridLayout_2.addWidget(self.label_path, 5, 0, 1, 1)

        self.titleEdit = QLineEdit(NasAdd)
        self.titleEdit.setObjectName(u"titleEdit")

        self.gridLayout_2.addWidget(self.titleEdit, 1, 2, 1, 1)

        self.addressEdit = QLineEdit(NasAdd)
        self.addressEdit.setObjectName(u"addressEdit")

        self.gridLayout_2.addWidget(self.addressEdit, 2, 2, 1, 1)

        self.label_pass = QLabel(NasAdd)
        self.label_pass.setObjectName(u"label_pass")
        self.label_pass.setMinimumSize(QSize(80, 30))

        self.gridLayout_2.addWidget(self.label_pass, 7, 0, 1, 1)

        self.label = QLabel(NasAdd)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(80, 30))

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_select = QLabel(NasAdd)
        self.label_select.setObjectName(u"label_select")

        self.gridLayout_2.addWidget(self.label_select, 4, 0, 1, 1)

        self.passEdit = QLineEdit(NasAdd)
        self.passEdit.setObjectName(u"passEdit")

        self.gridLayout_2.addWidget(self.passEdit, 7, 2, 1, 1)

        self.label_6 = QLabel(NasAdd)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(80, 90))

        self.gridLayout_2.addWidget(self.label_6, 10, 0, 1, 1)

        self.label_user = QLabel(NasAdd)
        self.label_user.setObjectName(u"label_user")
        self.label_user.setMinimumSize(QSize(80, 30))

        self.gridLayout_2.addWidget(self.label_user, 6, 0, 1, 1)

        self.label_5 = QLabel(NasAdd)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(80, 30))

        self.gridLayout_2.addWidget(self.label_5, 8, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.isWaifu2x = QCheckBox(NasAdd)
        self.isWaifu2x.setObjectName(u"isWaifu2x")

        self.horizontalLayout_2.addWidget(self.isWaifu2x)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 10, 2, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.dir1Radio = QRadioButton(NasAdd)
        self.buttonGroup = QButtonGroup(NasAdd)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.dir1Radio)
        self.dir1Radio.setObjectName(u"dir1Radio")
        self.dir1Radio.setChecked(True)

        self.horizontalLayout_5.addWidget(self.dir1Radio)

        self.dir2Radio = QRadioButton(NasAdd)
        self.buttonGroup.addButton(self.dir2Radio)
        self.dir2Radio.setObjectName(u"dir2Radio")

        self.horizontalLayout_5.addWidget(self.dir2Radio)

        self.dir3Radio = QRadioButton(NasAdd)
        self.buttonGroup.addButton(self.dir3Radio)
        self.dir3Radio.setObjectName(u"dir3Radio")

        self.horizontalLayout_5.addWidget(self.dir3Radio)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 9, 2, 1, 1)

        self.portEdit = QLineEdit(NasAdd)
        self.portEdit.setObjectName(u"portEdit")

        self.gridLayout_2.addWidget(self.portEdit, 3, 2, 1, 1)

        self.label_10 = QLabel(NasAdd)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(80, 30))

        self.gridLayout_2.addWidget(self.label_10, 9, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.dirButton = QPushButton(NasAdd)
        self.dirButton.setObjectName(u"dirButton")

        self.horizontalLayout_6.addWidget(self.dirButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)


        self.gridLayout_2.addLayout(self.horizontalLayout_6, 4, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.label_7 = QLabel(NasAdd)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout.addWidget(self.label_7)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.saveButton = QPushButton(NasAdd)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setMaximumSize(QSize(150, 30))
        self.saveButton.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.saveButton)

        self.testButton = QPushButton(NasAdd)
        self.testButton.setObjectName(u"testButton")
        self.testButton.setMaximumSize(QSize(150, 30))

        self.horizontalLayout_3.addWidget(self.testButton)

        self.closeButton = QPushButton(NasAdd)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMaximumSize(QSize(150, 30))

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        QWidget.setTabOrder(self.comboBox, self.titleEdit)
        QWidget.setTabOrder(self.titleEdit, self.addressEdit)
        QWidget.setTabOrder(self.addressEdit, self.pathEdit)
        QWidget.setTabOrder(self.pathEdit, self.userEdit)
        QWidget.setTabOrder(self.userEdit, self.passEdit)
        QWidget.setTabOrder(self.passEdit, self.compress1Radio)
        QWidget.setTabOrder(self.compress1Radio, self.dir1Radio)
        QWidget.setTabOrder(self.dir1Radio, self.dir2Radio)
        QWidget.setTabOrder(self.dir2Radio, self.dir3Radio)
        QWidget.setTabOrder(self.dir3Radio, self.isWaifu2x)
        QWidget.setTabOrder(self.isWaifu2x, self.saveButton)
        QWidget.setTabOrder(self.saveButton, self.testButton)
        QWidget.setTabOrder(self.testButton, self.closeButton)

        self.retranslateUi(NasAdd)

        QMetaObject.connectSlotsByName(NasAdd)
    # setupUi

    def retranslateUi(self, NasAdd):
        NasAdd.setWindowTitle(QCoreApplication.translate("NasAdd", u"Form", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("NasAdd", u"WebDav", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("NasAdd", u"SMB", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("NasAdd", u"\u672c\u5730\u8def\u5f84", None))

        self.pathEdit.setText(QCoreApplication.translate("NasAdd", u"/\u6d4b\u8bd5/\u957f\u7bc7/", None))
        self.pathEdit.setPlaceholderText("")
        self.label_port.setText(QCoreApplication.translate("NasAdd", u"\u7aef\u53e3", None))
        self.label_address.setText(QCoreApplication.translate("NasAdd", u"\u5730\u5740", None))
        self.userEdit.setText(QCoreApplication.translate("NasAdd", u"test", None))
        self.userEdit.setPlaceholderText("")
        self.label_8.setText(QCoreApplication.translate("NasAdd", u"\u5b58\u50a8\u540d/\u522b\u540d", None))
        self.compress1Radio.setText(QCoreApplication.translate("NasAdd", u"Zip", None))
        self.compress2Radio.setText(QCoreApplication.translate("NasAdd", u"cbz(\u5e26\u6f2b\u753b\u4fe1\u606f)", None))
        self.label_path.setText(QCoreApplication.translate("NasAdd", u"\u8def\u5f84", None))
#if QT_CONFIG(tooltip)
        self.titleEdit.setToolTip(QCoreApplication.translate("NasAdd", u"\u957f\u7bc7", None))
#endif // QT_CONFIG(tooltip)
        self.titleEdit.setText(QCoreApplication.translate("NasAdd", u"\u957f\u7bc7", None))
        self.titleEdit.setPlaceholderText("")
        self.addressEdit.setText(QCoreApplication.translate("NasAdd", u"http://192.168.31.28", None))
        self.addressEdit.setPlaceholderText("")
        self.label_pass.setText(QCoreApplication.translate("NasAdd", u"\u5bc6\u7801", None))
        self.label.setText(QCoreApplication.translate("NasAdd", u"\u534f\u8bae", None))
        self.label_select.setText(QCoreApplication.translate("NasAdd", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.passEdit.setText(QCoreApplication.translate("NasAdd", u"test", None))
        self.passEdit.setPlaceholderText("")
        self.label_6.setText(QCoreApplication.translate("NasAdd", u"\u5176\u4ed6\u8bbe\u7f6e", None))
        self.label_user.setText(QCoreApplication.translate("NasAdd", u"\u7528\u6237\u540d", None))
        self.label_5.setText(QCoreApplication.translate("NasAdd", u"\u6253\u5305\u65b9\u5f0f", None))
        self.isWaifu2x.setText(QCoreApplication.translate("NasAdd", u"\u4f7f\u7528\u4e0b\u8f7d\u4e2d\u8d85\u5206\u540e\u56fe\u7247", None))
        self.dir1Radio.setText(QCoreApplication.translate("NasAdd", u"\u4e0d\u5355\u72ec\u65b0\u589e\u76ee\u5f55", None))
        self.dir2Radio.setText(QCoreApplication.translate("NasAdd", u"\u6bcf\u672c\u6f2b\u753b\u5355\u72ec\u76ee\u5f55", None))
        self.dir3Radio.setText(QCoreApplication.translate("NasAdd", u"\u6309\u6dfb\u52a0\u65e5\u671f\u5206\u76ee\u5f55", None))
        self.portEdit.setText(QCoreApplication.translate("NasAdd", u"5005", None))
        self.label_10.setText(QCoreApplication.translate("NasAdd", u"\u76ee\u5f55\u8bbe\u7f6e", None))
        self.dirButton.setText(QCoreApplication.translate("NasAdd", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.label_7.setText("")
        self.saveButton.setText(QCoreApplication.translate("NasAdd", u"\u786e\u5b9a", None))
#if QT_CONFIG(shortcut)
        self.saveButton.setShortcut(QCoreApplication.translate("NasAdd", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.testButton.setText(QCoreApplication.translate("NasAdd", u"\u6d4b\u8bd5\u8fde\u63a5", None))
        self.closeButton.setText(QCoreApplication.translate("NasAdd", u"\u5173\u95ed", None))
    # retranslateUi

