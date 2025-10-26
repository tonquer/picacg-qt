# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_batch_sr.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidgetItem, QToolButton,
    QVBoxLayout, QWidget)

from component.box.wheel_combo_box import WheelComboBox
from component.box.wheel_double_spin_box import WheelDoubleSpinBox
from component.tab.base_table_widget import BaseTableWidget

class Ui_BatchSrTool(object):
    def setupUi(self, BatchSrTool):
        if not BatchSrTool.objectName():
            BatchSrTool.setObjectName(u"BatchSrTool")
        BatchSrTool.resize(800, 508)
        self.verticalLayout = QVBoxLayout(BatchSrTool)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(BatchSrTool)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.inputDir = QLineEdit(BatchSrTool)
        self.inputDir.setObjectName(u"inputDir")

        self.horizontalLayout_6.addWidget(self.inputDir)

        self.inputDirTool = QToolButton(BatchSrTool)
        self.inputDirTool.setObjectName(u"inputDirTool")

        self.horizontalLayout_6.addWidget(self.inputDirTool)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(BatchSrTool)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.exportDir = QLineEdit(BatchSrTool)
        self.exportDir.setObjectName(u"exportDir")

        self.horizontalLayout.addWidget(self.exportDir)

        self.exportDirTool = QToolButton(BatchSrTool)
        self.exportDirTool.setObjectName(u"exportDirTool")

        self.horizontalLayout.addWidget(self.exportDirTool)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(BatchSrTool)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.line_2 = QFrame(BatchSrTool)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_5.addWidget(self.line_2)

        self.label_25 = QLabel(BatchSrTool)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(60, 0))
        self.label_25.setMaximumSize(QSize(156, 16777215))

        self.horizontalLayout_5.addWidget(self.label_25)

        self.coverModelName = QToolButton(BatchSrTool)
        self.coverModelName.setObjectName(u"coverModelName")

        self.horizontalLayout_5.addWidget(self.coverModelName)

        self.line = QFrame(BatchSrTool)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_5.addWidget(self.line)

        self.label_26 = QLabel(BatchSrTool)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(60, 0))
        self.label_26.setMaximumSize(QSize(156, 16777215))

        self.horizontalLayout_5.addWidget(self.label_26)

        self.coverScale = WheelDoubleSpinBox(BatchSrTool)
        self.coverScale.setObjectName(u"coverScale")
        self.coverScale.setMinimumSize(QSize(150, 0))
        self.coverScale.setDecimals(1)
        self.coverScale.setMaximum(32.000000000000000)
        self.coverScale.setSingleStep(0.100000000000000)
        self.coverScale.setValue(2.000000000000000)

        self.horizontalLayout_5.addWidget(self.coverScale)

        self.line_3 = QFrame(BatchSrTool)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_5.addWidget(self.line_3)

        self.label_5 = QLabel(BatchSrTool)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.fmtBox = WheelComboBox(BatchSrTool)
        self.fmtBox.setObjectName(u"fmtBox")

        self.horizontalLayout_5.addWidget(self.fmtBox)

        self.line_4 = QFrame(BatchSrTool)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_5.addWidget(self.line_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.label_4 = QLabel(BatchSrTool)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.numLabel = QLabel(BatchSrTool)
        self.numLabel.setObjectName(u"numLabel")

        self.horizontalLayout_4.addWidget(self.numLabel)

        self.line_5 = QFrame(BatchSrTool)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_4.addWidget(self.line_5)

        self.label_6 = QLabel(BatchSrTool)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6)

        self.threadNum = QComboBox(BatchSrTool)
        self.threadNum.addItem("")
        self.threadNum.addItem("")
        self.threadNum.addItem("")
        self.threadNum.addItem("")
        self.threadNum.addItem("")
        self.threadNum.setObjectName(u"threadNum")

        self.horizontalLayout_4.addWidget(self.threadNum)

        self.startImportButton = QPushButton(BatchSrTool)
        self.startImportButton.setObjectName(u"startImportButton")
        self.startImportButton.setMaximumSize(QSize(150, 30))
        self.startImportButton.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.startImportButton)

        self.startConvertButton = QPushButton(BatchSrTool)
        self.startConvertButton.setObjectName(u"startConvertButton")
        self.startConvertButton.setMaximumSize(QSize(150, 30))

        self.horizontalLayout_4.addWidget(self.startConvertButton)

        self.cancleButton = QPushButton(BatchSrTool)
        self.cancleButton.setObjectName(u"cancleButton")
        self.cancleButton.setMaximumSize(QSize(150, 30))
        self.cancleButton.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.cancleButton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.tableWidget = BaseTableWidget(BatchSrTool)
        if (self.tableWidget.columnCount() < 6):
            self.tableWidget.setColumnCount(6)
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
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.msgLabel = QLabel(BatchSrTool)
        self.msgLabel.setObjectName(u"msgLabel")

        self.verticalLayout.addWidget(self.msgLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(BatchSrTool)

        self.threadNum.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(BatchSrTool)
    # setupUi

    def retranslateUi(self, BatchSrTool):
        BatchSrTool.setWindowTitle(QCoreApplication.translate("BatchSrTool", u"\u6279\u91cf\u8d85\u5206", None))
        self.label.setText(QCoreApplication.translate("BatchSrTool", u"\u5bfc\u5165\u76ee\u5f55\uff1a", None))
        self.inputDirTool.setText(QCoreApplication.translate("BatchSrTool", u"\u9009\u62e9", None))
        self.label_3.setText(QCoreApplication.translate("BatchSrTool", u"\u5bfc\u51fa\u76ee\u5f55\uff1a", None))
        self.exportDirTool.setText(QCoreApplication.translate("BatchSrTool", u"\u9009\u62e9", None))
        self.label_2.setText(QCoreApplication.translate("BatchSrTool", u"\u53c2\u6570\u8bbe\u7f6e\uff1a", None))
        self.label_25.setText(QCoreApplication.translate("BatchSrTool", u"\u6a21\u578b\uff1a", None))
        self.coverModelName.setText("")
        self.label_26.setText(QCoreApplication.translate("BatchSrTool", u"\u653e\u5927\u500d\u6570:", None))
        self.label_5.setText(QCoreApplication.translate("BatchSrTool", u"\u8f6c\u6362\u683c\u5f0f\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("BatchSrTool", u"\u6210\u529f/\u5931\u8d25/\u603b", None))
        self.numLabel.setText("")
        self.label_6.setText(QCoreApplication.translate("BatchSrTool", u"\u7ebf\u7a0b\u6570\uff1a", None))
        self.threadNum.setItemText(0, QCoreApplication.translate("BatchSrTool", u"1", None))
        self.threadNum.setItemText(1, QCoreApplication.translate("BatchSrTool", u"2", None))
        self.threadNum.setItemText(2, QCoreApplication.translate("BatchSrTool", u"3", None))
        self.threadNum.setItemText(3, QCoreApplication.translate("BatchSrTool", u"4", None))
        self.threadNum.setItemText(4, QCoreApplication.translate("BatchSrTool", u"5", None))

        self.startImportButton.setText(QCoreApplication.translate("BatchSrTool", u"\u5f00\u59cb\u5bfc\u5165", None))
#if QT_CONFIG(shortcut)
        self.startImportButton.setShortcut(QCoreApplication.translate("BatchSrTool", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.startConvertButton.setText(QCoreApplication.translate("BatchSrTool", u"\u5f00\u59cb\u8f6c\u6362", None))
        self.cancleButton.setText(QCoreApplication.translate("BatchSrTool", u"\u53d6\u6d88", None))
#if QT_CONFIG(shortcut)
        self.cancleButton.setShortcut(QCoreApplication.translate("BatchSrTool", u"Return", None))
#endif // QT_CONFIG(shortcut)
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("BatchSrTool", u"id", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("BatchSrTool", u"\u65f6\u95f4", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("BatchSrTool", u"\u72b6\u6001", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("BatchSrTool", u"\u9519\u8bef\u4fe1\u606f", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("BatchSrTool", u"\u6587\u4ef6\u540d", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("BatchSrTool", u"\u6587\u4ef6\u8def\u5f84", None));
        self.msgLabel.setText("")
    # retranslateUi

