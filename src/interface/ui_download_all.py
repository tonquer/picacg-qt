# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_download_all.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QTableWidgetItem, QVBoxLayout,
    QWidget)

from component.tab.base_table_widget import BaseTableWidget

class Ui_DownloadAll(object):
    def setupUi(self, DownloadAll):
        if not DownloadAll.objectName():
            DownloadAll.setObjectName(u"DownloadAll")
        DownloadAll.resize(543, 300)
        self.verticalLayout = QVBoxLayout(DownloadAll)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.selectAllButton = QPushButton(DownloadAll)
        self.selectAllButton.setObjectName(u"selectAllButton")
        self.selectAllButton.setMaximumSize(QSize(150, 30))
        self.selectAllButton.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.selectAllButton)

        self.chipButton = QPushButton(DownloadAll)
        self.chipButton.setObjectName(u"chipButton")
        self.chipButton.setMaximumSize(QSize(150, 30))

        self.horizontalLayout_4.addWidget(self.chipButton)

        self.downButton = QPushButton(DownloadAll)
        self.downButton.setObjectName(u"downButton")
        self.downButton.setMaximumSize(QSize(150, 30))
        self.downButton.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.downButton)

        self.uploadButton = QPushButton(DownloadAll)
        self.uploadButton.setObjectName(u"uploadButton")
        self.uploadButton.setMaximumSize(QSize(150, 30))

        self.horizontalLayout_4.addWidget(self.uploadButton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.tableWidget = BaseTableWidget(DownloadAll)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
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
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.msgLabel = QLabel(DownloadAll)
        self.msgLabel.setObjectName(u"msgLabel")

        self.verticalLayout.addWidget(self.msgLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(DownloadAll)

        QMetaObject.connectSlotsByName(DownloadAll)
    # setupUi

    def retranslateUi(self, DownloadAll):
        DownloadAll.setWindowTitle(QCoreApplication.translate("DownloadAll", u"\u6279\u91cf\u4e0b\u8f7d", None))
        self.selectAllButton.setText(QCoreApplication.translate("DownloadAll", u"\u4e00\u952e\u5168\u9009/\u53cd\u9009", None))
#if QT_CONFIG(shortcut)
        self.selectAllButton.setShortcut(QCoreApplication.translate("DownloadAll", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.chipButton.setText(QCoreApplication.translate("DownloadAll", u"\u4e00\u952e\u5168\u672c/\u5355\u7ae0", None))
        self.downButton.setText(QCoreApplication.translate("DownloadAll", u"\u5f00\u59cb\u4e0b\u8f7d", None))
#if QT_CONFIG(shortcut)
        self.downButton.setShortcut(QCoreApplication.translate("DownloadAll", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.uploadButton.setText(QCoreApplication.translate("DownloadAll", u"\u7f51\u7edc\u5b58\u50a8", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("DownloadAll", u"\u9009\u62e9", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("DownloadAll", u"\u4e0b\u8f7d\u5168\u672c/\u5355\u7ae0", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("DownloadAll", u"\u56fe\u7247\u6570", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("DownloadAll", u"\u5206\u7c7b", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("DownloadAll", u"\u540d\u79f0", None));
        self.msgLabel.setText("")
    # retranslateUi

