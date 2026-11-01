import os
import time
from distutils.dir_util import create_tree
from functools import partial

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, QRectF, QPointF, QSizeF, QEvent, QPoint, QTimer
from PySide6.QtGui import QPainter, QPixmap, QDoubleValidator, \
    QIntValidator, QMouseEvent, QImage, QAction, QCursor
from PySide6.QtWidgets import QFrame, QGraphicsPixmapItem, QGraphicsScene, QApplication, QFileDialog, QLabel, \
    QGraphicsView, QTableWidgetItem, QAbstractItemView, QHeaderView, QMenu, QComboBox, QPushButton

from component.box.wheel_combo_box import WheelComboBox
from config import config
from config.setting import Setting, SettingValue
from interface.ui_format_widget import Ui_FormatWidget
from interface.ui_waifu2x_tool import Ui_Waifu2xTool
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from task.task_local import LocalData
from tools.log import Log
from tools.str import Str
from component.dialog.base_mask_dialog import BaseMaskDialog


class DownloadFormatWidget(BaseMaskDialog, Ui_FormatWidget):
    def __init__(self, parent):
        BaseMaskDialog.__init__(self, parent)
        Ui_FormatWidget.__init__(self)
        self.widget.adjustSize()
        self.setupUi(self.widget)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.customContextMenuRequested.connect(self.SelectMenu)
        self.pushButton.clicked.connect(self.Add)
        self.saveButton.clicked.connect(self.Save)
        self.tableWidget.verticalHeader().setDefaultSectionSize(35)
        self.tableWidget.resizeRowsToContents()
        self.typeList = ["全部", "下载", "超分"]
        self.formatList = ["*", "png", "jpg", "webp", "gif", "jxl", "avif", "bmp"]
        self.toFormatList = ["png", "jpg", "webp", "gif", "jxl", "avif", "bmp"]
        self._Load()

    def _Load(self):
        for v in Setting.DownloadConvertFmt.value.split(":"):
            v2 = v.split(",")
            if len(v2) < 3:
                continue
            indexType = int(v2[0])
            format1 = v2[1]
            toFormat = v2[2]
            self.Add(indexType, format1, toFormat)

    # 右键菜单
    def SelectMenu(self, pos):
        menu = QMenu(self.tableWidget)
        addAction = QAction(Str.GetStr(Str.Add), self)
        addAction.triggered.connect(self.Add)

        delAction = QAction(Str.GetStr(Str.Delete), self)
        delAction.triggered.connect(self.Delete)
        menu.addAction(addAction)
        menu.addAction(delAction)
        menu.exec_(QCursor.pos())

    def Add(self, typeIndex=0, format="", toFormat=""):
        row_count = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row_count + 1)
        combo_box = WheelComboBox()
        combo_box.addItems(self.typeList)
        combo_box.setCurrentIndex(typeIndex)

        # combo_box.installEventFilter(self)
        self.tableWidget.setCellWidget(row_count, 0, combo_box)
        combo_box = WheelComboBox()
        combo_box.addItems(self.formatList)
        # combo_box.installEventFilter(self)
        if format in self.formatList:
            index = self.formatList.index(format)
            combo_box.setCurrentIndex(index)
        self.tableWidget.setCellWidget(row_count, 1, combo_box)
        combo_box = WheelComboBox()
        combo_box.addItems(self.toFormatList)
        # combo_box.installEventFilter(self)
        if toFormat in self.toFormatList:
            index = self.toFormatList.index(toFormat)
            combo_box.setCurrentIndex(index)
        self.tableWidget.setCellWidget(row_count, 2, combo_box)

        combo_box = QPushButton()
        combo_box.setText(Str.GetStr(Str.Delete))
        combo_box.clicked.connect(partial(self.DeleteByIndex, row_count))

        self.tableWidget.setCellWidget(row_count, 3, combo_box)
        self.tableWidget.resizeRowsToContents()
        return

    def DeleteByIndex(self, row):
        if row >= 0:
            self.tableWidget.removeRow(row)

    def Delete(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in sorted(selectRows, reverse=True):
            if row >= 0:
                self.tableWidget.removeRow(row)
        return

    def Save(self):
        settingList = []
        row_count = self.tableWidget.rowCount()
        isHaveAllDown = False
        isHaveAllConvet = False
        for i in range(row_count):
            typeBox = self.tableWidget.cellWidget(i, 0)
            assert isinstance(typeBox, WheelComboBox)
            formatBox = self.tableWidget.cellWidget(i, 1)
            assert isinstance(formatBox, WheelComboBox)
            if formatBox.currentText() == "*":
                if typeBox.currentIndex() == 0:
                    if isHaveAllDown or isHaveAllConvet:
                        QtOwner().ShowMsg(Str.GetStr(Str.RepeatRule))
                        return
                    isHaveAllDown = True
                    isHaveAllConvet = True
                elif typeBox.currentIndex() == 1:
                    if isHaveAllDown:
                        QtOwner().ShowMsg(Str.GetStr(Str.RepeatRule))
                        return
                    isHaveAllDown = True
                elif typeBox.currentIndex() == 2:
                    if isHaveAllConvet:
                        QtOwner().ShowMsg(Str.GetStr(Str.RepeatRule))
                        return
                    isHaveAllConvet = True

            toFormatBox = self.tableWidget.cellWidget(i, 2)
            assert isinstance(toFormatBox, WheelComboBox)
            settingList.append(",".join([str(typeBox.currentIndex()), formatBox.currentText(), toFormatBox.currentText()]))
        Setting.DownloadConvertFmt.SetValue(":".join(settingList))
        QtOwner().UpdateConvertFmtRule()
        QtOwner().UpdateDownFmtRule()

        QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        self.close()
        return

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.ContextMenu):
            return False
        return BaseMaskDialog.eventFilter(self, obj, event)
