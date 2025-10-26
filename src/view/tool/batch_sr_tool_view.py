import os
import time
from distutils.dir_util import create_tree
from functools import partial

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, QRectF, QPointF, QSizeF, QEvent, QPoint, QTimer
from PySide6.QtGui import QPainter, QPixmap, QDoubleValidator, \
    QIntValidator, QMouseEvent, QImage
from PySide6.QtWidgets import QFrame, QGraphicsPixmapItem, QGraphicsScene, QApplication, QFileDialog, QLabel, \
    QGraphicsView, QTableWidgetItem, QAbstractItemView, QHeaderView

from config import config
from config.setting import Setting, SettingValue
from interface.ui_batch_sr import Ui_BatchSrTool
from interface.ui_waifu2x_tool import Ui_Waifu2xTool
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from task.task_local import LocalData
from tools.log import Log
from tools.str import Str
from tools.tool import ToolUtil
from view.read.read_qgraphics_proxy_widget import ReadQGraphicsProxyWidget
from view.tool.batch_sr_tool_db import BatchSrToolDb


class BatchSrItem(QtTaskBase):
    Pause = Str.Pause
    Converting = Str.Converting
    ConvertSuccess = Str.ConvertSuccess
    Error = Str.Error

    def __init__(self):
        QtTaskBase.__init__(self)
        self.index = 0             # 索引
        self.path = ""              # 路径
        self.fileName = ""          # 文件名
        self.addTime = int(time.time())                #
        self.tick = ""            #
        self.status = 0           #
        self.msg = ""             #
        self.fmt = ""

class BatchSrToolView(QtWidgets.QWidget, Ui_BatchSrTool, QtTaskBase):
    NotSelect = 0       # 未选择目录
    StartImport = 1     # 点击开始导入
    AlreadyImport = 2   # 已导入
    StartConvert = 3    # 开始转换
    PauseConvert = 4    # 暂停转换
    Success  = 5         # 完成

    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_BatchSrTool.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        self.curState = self.NotSelect

        self.inputDirPath = ""
        self.exportDirPath = ""
        self.allItem = {}

        self.convertingIndex = set()
        self.db  = BatchSrToolDb()
        self.allItem = {}
        self.indexToRow = {}
        self.timer = QTimer(self.tableWidget)
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.TimeOutHandler)
        self.inputDirTool.clicked.connect(partial(self.SelectSavePath, self.inputDir))
        self.exportDirTool.clicked.connect(partial(self.SelectSavePath, self.exportDir))
        self.startConvertButton.clicked.connect(self.StartItemConvert)
        self.startImportButton.clicked.connect(self.StartItemImportDir)
        self.cancleButton.clicked.connect(self.CancleItemConvert)
        self.fmtBox.addItem("")
        for fmt in ["png", "jpg", "webp", "apng", "bmp"]:
            self.fmtBox.addItem(fmt)

        self.order = {}
        self.coverModelName.clicked.connect(self.CheckOpenSrSelect)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.Sort)
        # self.tableWidget.setColumnHidden(0, True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.inputDir.editingFinished.connect(partial(self.LineEditEvent, Setting.BatchSrImportDir, self.inputDir))
        self.exportDir.editingFinished.connect(
            partial(self.LineEditEvent, Setting.BatchSrExportDir, self.exportDir))

        self.coverScale.valueChanged.connect(partial(self.SpinBoxEvent, Setting.BatchSrScale))

        self.fmtBox.currentTextChanged.connect(partial(self.CheckRadioEvent, Setting.BatchSrFmt))
        self.maxConvertNum = 2
        self.threadNum.currentIndexChanged.connect(self.UpdateThreadNum)

    def UpdateThreadNum(self, index):
        self.maxConvertNum = self.threadNum.currentIndex() + 1

    def CheckRadioEvent(self, setItem, value):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(value)
        return

    def LineEditEvent(self, setItem, lineEdit):
        assert isinstance(setItem, SettingValue)
        value = lineEdit.text()
        setItem.SetValue(value)
        return

    def SpinBoxEvent(self, setItem, value):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(int(value))
        return

    def CheckOpenSrSelect(self):
        QtOwner().OpenSrSelectModel(self.coverModelName.text(), self.CheckOpenSrSelectCoverBack)

    def CheckOpenSrSelectCoverBack(self, modelName):
        self.coverModelName.setText(modelName)
        Setting.BatchSrModelName.SetValue(modelName)
        return modelName

    def SelectSavePath(self, lineEdit):
        url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold))
        if url:
            lineEdit.setText(url)
            if lineEdit == self.inputDir:
                self.exportDir.setText(url+"(sr)")
            self.LineEditEvent(Setting.BatchSrImportDir, self.inputDir)
            self.LineEditEvent(Setting.BatchSrExportDir, self.exportDir)

    def retranslateUi(self, SettingNew):
        Ui_BatchSrTool.retranslateUi(self, SettingNew)

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if not self.isInit:
            self.Init()
        return

    def Init(self):
        self.isInit = True
        if Setting.BatchSrState.value:

            self.curState = int(Setting.BatchSrState.value)
        self.exportDirPath = Setting.BatchSrExportDir.value
        self.inputDirPath = Setting.BatchSrImportDir.value

        self.exportDir.setText(self.exportDirPath)
        self.inputDir.setText(self.inputDirPath)
        self.fmtBox.setCurrentText(Setting.BatchSrFmt.value)
        self.coverModelName.setText(Setting.BatchSrModelName.value)
        self.coverScale.setValue(Setting.BatchSrScale.value)

        if self.curState == self.StartImport:
            self.curState = self.NotSelect
        if self.curState == self.StartConvert:
            self.curState = self.PauseConvert
        allData = self.db.LoadBatchSrItem()
        self.allItem = allData
        for item in sorted(self.allItem.values(), key=lambda a: a.index):
            if item.status == item.Converting:
                item.status = 0
            rowCont = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCont)
            self.indexToRow[item.index] = rowCont
            self.UpdateTableItem(item)
        self.UpdateConvertLabel()
        self.UpdateEnable()
        self.UpdateProcessLabel()
        return

    def SaveSetting(self):
        Setting.BatchSrState.SetValue(self.curState)
        Setting.BatchSrExportDir.SetValue(self.exportDirPath)
        Setting.BatchSrImportDir.SetValue(self.inputDirPath)
        Setting.BatchSrFmt.SetValue(self.fmtBox.currentText())
        return

    def UpdateEnable(self):
        self.inputDir.setEnabled(True)
        self.inputDirTool.setEnabled(True)
        self.exportDir.setEnabled(True)
        self.exportDirTool.setEnabled(True)
        self.fmtBox.setEnabled(True)

        self.startConvertButton.setEnabled(True)
        self.startImportButton.setEnabled(True)
        self.cancleButton.setEnabled(True)
        self.coverModelName.setEnabled(True)
        self.coverScale.setEnabled(True)

        if self.curState == self.NotSelect:
            self.cancleButton.setEnabled(False)
            self.startConvertButton.setEnabled(False)
        elif self.curState == self.StartImport:
            self.startImportButton.setEnabled(False)
            self.startConvertButton.setEnabled(False)
            self.inputDir.setEnabled(False)
            self.inputDirTool.setEnabled(False)
            self.exportDir.setEnabled(False)
            self.exportDirTool.setEnabled(False)

        elif self.curState == self.AlreadyImport:
            self.startImportButton.setEnabled(False)
            self.inputDir.setEnabled(False)
            self.inputDirTool.setEnabled(False)
            self.exportDir.setEnabled(False)
            self.exportDirTool.setEnabled(False)
        elif self.curState == self.StartConvert:
            self.startImportButton.setEnabled(False)
            self.coverModelName.setEnabled(False)
            self.coverScale.setEnabled(False)
            self.fmtBox.setEnabled(False)
            self.inputDir.setEnabled(False)
            self.inputDirTool.setEnabled(False)
            self.exportDir.setEnabled(False)
            self.exportDirTool.setEnabled(False)
        elif self.curState == self.PauseConvert:
            self.startImportButton.setEnabled(False)
            self.coverModelName.setEnabled(False)
            self.coverScale.setEnabled(False)
            self.inputDir.setEnabled(False)
            self.inputDirTool.setEnabled(False)
            self.exportDir.setEnabled(False)
            self.exportDirTool.setEnabled(False)
        elif self.curState == self.Success:
            self.startImportButton.setEnabled(False)
            self.coverModelName.setEnabled(False)
            self.coverScale.setEnabled(False)
            self.fmtBox.setEnabled(False)
            # self.startConvertButton.setEnabled(False)
            self.inputDir.setEnabled(False)
            self.inputDirTool.setEnabled(False)
            self.exportDir.setEnabled(False)
            self.exportDirTool.setEnabled(False)

    def UpdateProcessLabel(self):
        num = 0
        complete = 0
        fail = 0
        for item in self.allItem.values():
            assert isinstance(item, BatchSrItem)
            if item.status == item.ConvertSuccess:
                complete += 1
            elif item.status == item.Error:
                fail += 1
            num += 1
        self.numLabel.setText(f"{complete}/{fail}/{num}")

    def UpdateConvertLabel(self):
        if self.curState == self.StartConvert:
            self.startConvertButton.setText(Str.GetStr(Str.Pause))
        else:
            for data in self.allItem.values():
                assert isinstance(data, BatchSrItem)
                if data.status == data.Error:
                    data.status = 0
                    self.UpdateTableItem(data)
            self.startConvertButton.setText(Str.GetStr(Str.Convert))

    def SwitchState(self, newState):
        if self.curState == newState:
            return
        self.curState = newState
        Setting.BatchSrState.SetValue(newState)
        self.UpdateEnable()

    def StartItemImportDir(self):
        dirName = self.inputDir.text()
        if not dirName:
            QtOwner().ShowError(Str.GetStr(Str.SrNotFoundDir))
            return
        if not os.path.isdir(dirName):
            QtOwner().ShowError(Str.GetStr(Str.SrNotFoundDir))
            return
        exportName = self.exportDir.text()
        if not exportName:
            QtOwner().ShowError(Str.GetStr(Str.SrNotExportDIr))
            return
        if dirName == exportName:
            QtOwner().ShowError(Str.GetStr(Str.SrNotExportDIr))
            return
        self.allItem.clear()
        self.db.ClearBatchSrItem()
        self.indexToRow.clear()

        self.inputDirPath = dirName
        self.exportDirPath = exportName
        for i in range(self.tableWidget.rowCount(), 0, -1):
            self.tableWidget.removeRow(i-1)

        self.SwitchState(self.StartImport)
        self.AddLocalTaskLoad(LocalData.TypeLoadPicFile, dirName, 0, callBack=self.StartImportDirBack)
        return

    def StartImportDirBack(self, st, fileNames, _):
        if st == Str.Waiting:
            for path, name in fileNames:
                item = BatchSrItem()
                if not self.indexToRow:
                    index = 1
                else:
                    index = max(self.indexToRow.keys())+1
                item.index = index
                item.path = path
                item.fileName = name
                data = name.split(".")
                if len(data) < 2:
                    mat = ""
                else:
                    mat = data[-1]
                item.fmt = mat
                rowCont = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowCont)
                self.indexToRow[item.index] = rowCont
                self.allItem[item.index] = item
                self.db.AddBatchSrItem(item)
                self.UpdateTableItem(item)

            return
        elif st == Str.Ok:
            self.SwitchState(self.AlreadyImport)
        self.UpdateProcessLabel()
        return

    def StartItemConvert(self):
        if self.curState == self.StartConvert:
            self.SwitchState(self.PauseConvert)
        else:
            self.SwitchState(self.StartConvert)
            if not self.timer.isActive():
                self.timer.start()
            self.TimeOutHandler()
        self.UpdateConvertLabel()
        return

    def PauseItemConvert(self):
        self.SwitchState(self.PauseConvert)
        self.convertingIndex.clear()
        self.ClearConvert()
        return

    def CancleItemConvert(self):
        self.SwitchState(self.NotSelect)
        for i in range(self.tableWidget.rowCount(), 0, -1):
            self.tableWidget.removeRow(i-1)
        self.db.ClearBatchSrItem()
        return

    def UpdateTableItem(self, info):
        assert isinstance(info, BatchSrItem)
        row = self.indexToRow.get(info.index, -1)
        if row < 0:
            return
        self.tableWidget.setItem(row, 0, QTableWidgetItem(str(info.index)))
        if info.tick:
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(info.tick) + "s"))
        else:
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(info.tick)))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(Str.GetStr(info.status)))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(info.msg))
        # self.tableWidget.setItem(row, 4, QTableWidgetItem(info.fmt))
        self.tableWidget.setItem(row, 4, QTableWidgetItem(info.fileName))
        self.tableWidget.setItem(row, 5, QTableWidgetItem(info.path))
        return

    def TimeOutHandler(self):
        if self.curState != self.StartConvert:
            return

        downloadNum = self.maxConvertNum
        addNum = downloadNum - len(self.convertingIndex)

        allFinish = True
        if addNum > 0:
            for task in self.allItem.values():
                assert isinstance(task, BatchSrItem)
                if task.status == task.ConvertSuccess:
                    continue
                if task.status == task.Error:
                    continue
                if task.status == task.Converting:
                    continue
                if task.index in self.convertingIndex:
                    continue
                allFinish = False
                self.StartItemConvertToTask(task)
                addNum -= 1
                if addNum <= 0:
                    break
        if allFinish and not self.convertingIndex:
            self.SwitchState(self.Success)
            self.UpdateConvertLabel()

    def StartItemConvertToTask(self, task):
        self.convertingIndex.add(task.index)
        assert isinstance(task, BatchSrItem)
        task.status = task.Converting
        loadPath = os.path.join(os.path.join(self.inputDirPath, task.path), task.fileName)
        if Setting.BatchSrFmt.value:
            data = task.fileName.split(".")
            data[-1] = Setting.BatchSrFmt.value
            toFilename = ".".join(data)
        else:
            toFilename = task.fileName
        savePath = os.path.join(os.path.join(self.exportDirPath, task.path), toFilename)
        model = ToolUtil.GetModelByIndex(Setting.BatchSrModelName.value, Setting.BatchSrScale.value)
        model['isForce'] = 1
        model['format'] = Setting.BatchSrFmt.value
        self.AddConvertTaskByPathSetModel(loadPath, savePath, self.StartItemConvertBack, task.index, model=model, cleanFlag=task.cleanFlag)
        self.UpdateTableItem(task)
        self.db.AddBatchSrItem(task)
        return

    def StartItemConvertBack(self, data, st, index, tick):
        if index not in self.allItem:
            return
        task = self.allItem.get(index)
        if index in self.convertingIndex:
            self.convertingIndex.discard(index)

        assert isinstance(task, BatchSrItem)
        if st == Str.Ok:
            task.tick = tick
            task.status = task.ConvertSuccess

            self.db.AddBatchSrItem(task)

            self.TimeOutHandler()
        else:
            task.status = task.Error
            task.msg = Str.GetStr(st)
            self.db.AddBatchSrItem(task)
        self.UpdateTableItem(task)
        self.UpdateProcessLabel()
        return

    def Stop(self):
        self.timer.stop()

    def Sort(self, col):
        order = self.order.get(col, 1)
        if order == 1:
            self.tableWidget.sortItems(col, Qt.AscendingOrder)
            self.order[col] = 0
        else:
            self.tableWidget.sortItems(col, Qt.DescendingOrder)
            self.order[col] = 1
        self.UpdateTableRow()


    def UpdateTableRow(self):
        count = self.tableWidget.rowCount()
        for i in range(count):
            bookId = self.tableWidget.item(i, 0).text()
            info = self.allItem.get(int(bookId))
            if info:
                self.indexToRow[info.index] = i
