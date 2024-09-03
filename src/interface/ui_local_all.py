# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_local_all.ui'
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

class Ui_LocalAll(object):
    def setupUi(self, LocalAll):
        if not LocalAll.objectName():
            LocalAll.setObjectName(u"LocalAll")
        LocalAll.resize(541, 293)
        self.verticalLayout = QVBoxLayout(LocalAll)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.selectAllButton = QPushButton(LocalAll)
        self.selectAllButton.setObjectName(u"selectAllButton")
        self.selectAllButton.setMaximumSize(QSize(150, 30))
        self.selectAllButton.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.selectAllButton)

        self.downButton = QPushButton(LocalAll)
        self.downButton.setObjectName(u"downButton")
        self.downButton.setMaximumSize(QSize(150, 30))
        self.downButton.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.downButton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.tableWidget = BaseTableWidget(LocalAll)
        if (self.tableWidget.columnCount() < 7):
            self.tableWidget.setColumnCount(7)
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
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.msgLabel = QLabel(LocalAll)
        self.msgLabel.setObjectName(u"msgLabel")

        self.verticalLayout.addWidget(self.msgLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(LocalAll)

        QMetaObject.connectSlotsByName(LocalAll)
    # setupUi

    def retranslateUi(self, LocalAll):
        LocalAll.setWindowTitle(QCoreApplication.translate("LocalAll", u"\u6279\u91cf\u4e0b\u8f7d", None))
        self.selectAllButton.setText(QCoreApplication.translate("LocalAll", u"\u4e00\u952e\u5168\u9009/\u53cd\u9009", None))
#if QT_CONFIG(shortcut)
        self.selectAllButton.setShortcut(QCoreApplication.translate("LocalAll", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.downButton.setText(QCoreApplication.translate("LocalAll", u"\u5220\u9664", None))
#if QT_CONFIG(shortcut)
        self.downButton.setShortcut(QCoreApplication.translate("LocalAll", u"Return", None))
#endif // QT_CONFIG(shortcut)
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("LocalAll", u"\u9009\u62e9", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("LocalAll", u"\u540d\u79f0", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("LocalAll", u"\u5206\u7c7b", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("LocalAll", u"\u56fe\u7247\u6570", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("LocalAll", u"\u6dfb\u52a0\u65e5\u671f", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("LocalAll", u"\u4e0a\u6b21\u89c2\u770b\u65f6\u95f4", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("LocalAll", u"ID", None));
        self.msgLabel.setText("")
    # retranslateUi

