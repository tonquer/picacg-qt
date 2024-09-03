# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_download.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QHeaderView, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QWidget)

class Ui_Download(object):
    def setupUi(self, Download):
        if not Download.objectName():
            Download.setObjectName(u"Download")
        Download.resize(920, 440)
        self.gridLayout_2 = QGridLayout(Download)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableWidget = QTableWidget(Download)
        if (self.tableWidget.columnCount() < 11):
            self.tableWidget.setColumnCount(11)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout.addWidget(self.tableWidget, 5, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.updateNew = QPushButton(Download)
        self.updateNew.setObjectName(u"updateNew")

        self.horizontalLayout.addWidget(self.updateNew)

        self.pushButton = QPushButton(Download)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(Download)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(Download)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_4 = QPushButton(Download)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout.addWidget(self.pushButton_4)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.redownloadRadio = QCheckBox(Download)
        self.redownloadRadio.setObjectName(u"redownloadRadio")

        self.horizontalLayout_2.addWidget(self.redownloadRadio)

        self.radioButton = QRadioButton(Download)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setEnabled(True)
        self.radioButton.setChecked(True)

        self.horizontalLayout_2.addWidget(self.radioButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)


        self.retranslateUi(Download)
        self.pushButton.clicked.connect(Download.StartAll)
        self.pushButton_3.clicked.connect(Download.StopAll)
        self.pushButton_2.clicked.connect(Download.StartConvertAll)
        self.pushButton_4.clicked.connect(Download.StopConvertAll)
        self.radioButton.clicked.connect(Download.SetAutoConvert)

        QMetaObject.connectSlotsByName(Download)
    # setupUi

    def retranslateUi(self, Download):
        Download.setWindowTitle(QCoreApplication.translate("Download", u"\u4e0b\u8f7d", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Download", u"id", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Download", u"\u65f6\u95f4", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Download", u"\u6807\u9898", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Download", u"\u4e0b\u8f7d\u8fdb\u5ea6", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Download", u"\u4e0b\u8f7d\u7ae0\u8282", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Download", u"\u4e0b\u8f7d\u901f\u5ea6", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Download", u"\u4e0b\u8f7d\u72b6\u6001", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Download", u"\u8f6c\u6362\u8fdb\u5ea6", None));
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Download", u"\u8f6c\u6362\u7ae0\u8282", None));
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Download", u"\u8f6c\u6362\u8017\u65f6", None));
        ___qtablewidgetitem10 = self.tableWidget.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Download", u"\u8f6c\u6362\u72b6\u6001", None));
        self.updateNew.setText(QCoreApplication.translate("Download", u"\u66f4\u65b0New\u7ae0\u8282", None))
        self.pushButton.setText(QCoreApplication.translate("Download", u"\u5f00\u59cb\u4e0b\u8f7d", None))
        self.pushButton_3.setText(QCoreApplication.translate("Download", u"\u6682\u505c\u4e0b\u8f7d", None))
        self.pushButton_2.setText(QCoreApplication.translate("Download", u"\u5f00\u59cb\u8f6c\u6362", None))
        self.pushButton_4.setText(QCoreApplication.translate("Download", u"\u6682\u505c\u8f6c\u6362", None))
        self.redownloadRadio.setText(QCoreApplication.translate("Download", u"\u4e0b\u8f7d\u5931\u8d25\u540e\u81ea\u52a8\u91cd\u8bd5", None))
        self.radioButton.setText(QCoreApplication.translate("Download", u"\u4e0b\u8f7d\u81ea\u52a8Waifu2x\u8f6c\u6362", None))
    # retranslateUi

