import os
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QPixmap, QImage, QCursor
from PySide6.QtWidgets import QMenu

from config import config
from config.setting import Setting
from qt_owner import QtOwner
from server import req, Status, Log
from task.qt_task import QtTaskBase
from tools.book import BookMgr
from tools.str import Str
from tools.tool import time_me, ToolUtil
from view.read.read_enum import ReadMode, QtFileData
from view.read.read_frame import ReadFrame


class ReadView(QtWidgets.QWidget, QtTaskBase):

    def __init__(self):
        super(self.__class__, self).__init__()
        QtTaskBase.__init__(self)
        self.bookId = ""
        self.token = ""
        self.epsId = 0
        self.resetCnt = config.ResetCnt
        self.curIndex = 0

        self.pictureData = {}
        self.maxPic = 0
        # desktop = QGuiApplication.primaryScreen().geometry()
        # self.resize(desktop.width() // 4 * 3, desktop.height() - 100)
        # self.move(desktop.width() // 8, 0)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = ReadFrame(self)
        # self.gridLayout.addWidget(self.scrollArea)
        self.gridLayout.addWidget(self.frame)
        self.setMinimumSize(300, 300)
        self.category = []
        self.isInit = False
        self.epsName = ""

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.SelectMenu)
        self.isShowMenu = False

        self.stripModel = ReadMode(Setting.LookReadMode.value)
        self.ChangeReadMode(Setting.LookReadMode.value)
        self.qtTool.turnSpeed.setValue(Setting.TurnSpeed.value / 1000)
        self.qtTool.scrollSpeed.setValue(Setting.ScrollSpeed.value)
        self.pageIndex = -1

    @property
    def scrollArea(self):
        return self.frame.scrollArea

    def retranslateUi(self, View):
        self.qtTool.retranslateUi(self.qtTool)

    def SelectMenu(self):
        popMenu = QMenu(self)
        action = popMenu.addAction(Str.GetStr(Str.Menu))
        action.triggered.connect(self.ShowAndCloseTool)

        action = popMenu.addAction(Str.GetStr(Str.FullSwitch))
        action.triggered.connect(self.qtTool.FullScreen)

        menu2 = popMenu.addMenu(Str.GetStr(Str.ReadMode))

        def AddReadMode(name, value):
            action = menu2.addAction(name)
            action.triggered.connect(partial(self.ChangeReadMode, value))
            if self.stripModel.value == value:
                action.setCheckable(True)
                action.setChecked(True)
        AddReadMode(Str.GetStr(Str.UpDownScroll), 0)
        AddReadMode(Str.GetStr(Str.Default), 1)
        AddReadMode(Str.GetStr(Str.LeftRightDouble), 2)
        AddReadMode(Str.GetStr(Str.RightLeftDouble), 3)
        AddReadMode(Str.GetStr(Str.LeftRightScroll), 4)
        AddReadMode(Str.GetStr(Str.RightLeftScroll), 5)

        menu3 = popMenu.addMenu(Str.GetStr(Str.Scale))

        def AddScaleMode(name, value):
            action = menu3.addAction(name)
            action.triggered.connect(partial(self.qtTool.ScalePicture, value))
            if (self.frame.scaleCnt + 10) * 10 == value:
                action.setCheckable(True)
                action.setChecked(True)

        AddScaleMode("50%", 50)
        AddScaleMode("60%", 60)
        AddScaleMode("70%", 70)
        AddScaleMode("80%", 80)
        AddScaleMode("90%", 90)
        AddScaleMode("100%", 100)
        AddScaleMode("120%", 120)
        AddScaleMode("140%", 140)
        AddScaleMode("160%", 160)
        AddScaleMode("180%", 180)
        AddScaleMode("200%", 200)

        menu3 = popMenu.addMenu(Str.GetStr(Str.SwitchPage))
        action = menu3.addAction(Str.GetStr(Str.LastChapter))
        action.triggered.connect(self.qtTool.OpenLastEps)
        action = menu3.addAction(Str.GetStr(Str.NextChapter))
        action.triggered.connect(self.qtTool.OpenNextEps)

        action = popMenu.addAction(Str.GetStr(Str.AutoScroll))
        action.triggered.connect(self.qtTool.SwitchScrollAndTurn)

        action = popMenu.addAction(Str.GetStr(Str.Exit))
        action.triggered.connect(self.Close)

        if self.qtTool.IsStartScrollAndTurn():
            action.setCheckable(True)
            action.setChecked(True)

        self.isShowMenu = True
        popMenu.exec_(QCursor.pos())

    @property
    def qtTool(self):
        return self.frame.qtTool

    def Close(self):
        self.ReturnPage()
        self.frame.scrollArea.ClearPixItem()
        self.Clear()
        if QtOwner().owner.windowState() == Qt.WindowFullScreen:
            self.qtTool.FullScreen(True)
        QtOwner().CloseReadView()
        QtOwner().bookInfoView.ReloadHistory.emit()
        QtOwner().SetSubTitle("")

    def Clear(self):
        Setting.TurnSpeed.SetValue(int(self.qtTool.turnSpeed.value() * 1000))
        Setting.ScrollSpeed.SetValue(int(self.qtTool.scrollSpeed.value()))
        self.qtTool.UpdateText("")
        self.frame.UpdateProcessBar(None)
        self.qtTool.CloseScrollAndTurn()
        self.bookId = ""
        self.epsId = 0
        self.maxPic = 0
        self.curIndex = 0
        self.frame.oldValue = 0
        self.pictureData.clear()
        QtOwner().SetSubTitle("")
        self.ClearTask()
        self.ClearDownload()
        self.ClearQImageTask()

    def OpenPage(self, bookId, epsId, name, pageIndex=-1):
        if not bookId:
            return
        self.Clear()
        info = BookMgr().books.get(bookId)
        if info:
            self.category = info.categories[::]

        self.qtTool.checkBox.setChecked(Setting.IsOpenWaifu.value)
        self.qtTool.SetData(isInit=True)
        self.qtTool.SetData()

        # self.qtTool.show()
        self.bookId = bookId
        self.epsId = epsId
        self.pageIndex = pageIndex

        self.qtTool.isMaxFull = self.window().isMaximized()
        if Setting.LookReadFull.value:
            QtOwner().owner.showFullScreen()
            self.qtTool.fullButton.setText(Str.GetStr(Str.ExitFullScreen))

        self.epsName = name
        QtOwner().ShowLoading()

        # 开始加载
        self.InitDownload()

        if config.IsTips:
            config.IsTips = 0
            self.frame.InitHelp()

    def ReturnPage(self):
        self.AddHistory()
        # QtOwner().owner.bookInfoForm.LoadHistory()
        return

    def CheckLoadPicture(self):
        # i = 0
        newDict = {}
        needUp = False
        removeTaskIds = []

        if not self.maxPic:
            return

        preLoadList = list(range(self.curIndex, self.curIndex + config.PreLoading))

        # 预加载上一页
        if len(preLoadList) >= 2 and self.curIndex > 0:
            preLoadList.insert(2, self.curIndex - 1)

        for i, p in self.pictureData.items():
            if i in preLoadList:
                newDict[i] = p
            else:
                needUp = True
                if p.waifu2xTaskId > 0:
                    removeTaskIds.append(p.waifu2xTaskId)

        if needUp:
            self.pictureData.clear()
            self.pictureData = newDict
            self.ClearWaitConvertIds(removeTaskIds)

        if not self.bookId:
            return

        for i in preLoadList:
            if i >= self.maxPic or i < 0:
                continue

            p = self.pictureData.get(i)
            if not p:
                self.AddDownload(i)
                break
            elif p.state == p.Downloading or p.state == p.DownloadReset:
                break

        for i in preLoadList:
            if i >= self.maxPic or i < 0:
                continue
            if Setting.IsOpenWaifu.value:
                p = self.pictureData.get(i)
                if not p or not p.data:
                    break
                if p.waifuState == p.WaifuStateCancle or p.waifuState == p.WaifuWait:
                    p.waifuState = p.WaifuStateStart
                    self.AddCovertData(i)
                    break
                if p.waifuState == p.WaifuStateStart:
                    break
        pass

    def StartLoadPicUrlBack(self, raw, v):
        st = raw["st"]
        if st == Status.Error:
            QtOwner().ShowError(Str.GetStr(st))
            return
        maxPic = raw.get("maxPic")
        if not maxPic or self.maxPic > 0:
            return
        self.maxPic = maxPic
        # info = BookMgr().GetBook(self.bookId)

        if 0 < self.pageIndex < self.maxPic:
            self.curIndex = self.pageIndex
            QtOwner().ShowMsg(Str.GetStr(Str.ContinueRead) + str(self.pageIndex + 1) + Str.GetStr(Str.Page))

        self.AddHistory()
        self.scrollArea.InitAllQLabel(self.maxPic, self.curIndex)
        self.qtTool.UpdateSlider()
        self.CheckLoadPicture()
        self.qtTool.InitSlider(self.maxPic)

        return

    def UpdateProcessBar(self, downloadSize, laveFileSize, backParam):
        info = self.pictureData.get(backParam)
        if not info:
            return
        if laveFileSize < 0:
            info.downloadSize = 0
        if info.size <= 0:
            info.size = laveFileSize
        info.downloadSize += downloadSize
        if self.curIndex != backParam:
            return
        self.frame.UpdateProcessBar(info)

    def CompleteDownloadPic(self, data, st, index):
        QtOwner().CloseLoading()
        p = self.pictureData.get(index)
        if not p:
            p = QtFileData()
            self.pictureData[index] = p
        if st != Status.Ok:
            p.state = p.DownloadReset
            self.AddDownload(index)
        else:
            p.SetData(data, self.category)
            self.AddQImageTask(data, self.ConvertQImageBack, index)
            self.CheckLoadPicture()

    def ConvertQImageBack(self, data, index):
        assert isinstance(data, QImage)
        p = self.pictureData.get(index)
        if not p:
            return
        assert isinstance(p, QtFileData)
        p.cacheImage = data
        if index == self.curIndex:
            self.ShowImg()
        elif self.stripModel in [ReadMode.UpDown, ReadMode.RightLeftScroll,
                                 ReadMode.LeftRightScroll] and self.curIndex < index <= self.curIndex + config.PreLoading - 1:
            self.ShowOtherPage()
        elif self.stripModel in [ReadMode.RightLeftDouble,
                                 ReadMode.LeftRightDouble] and self.curIndex < index <= self.curIndex + 1:
            self.ShowOtherPage()
        return

    def ShowPage(self, index):
        if index >= self.maxPic:
            return

        p = self.pictureData.get(index)
        if not p or (not p.data) or (not p.cacheImage):
            self.scrollArea.SetPixIem(index, None)
            return

        waifu2x = False
        assert isinstance(p, QtFileData)
        if not Setting.IsOpenWaifu.value:
            p2 = p.cacheImage

        elif p.cacheWaifu2xImage:
            waifu2x = True
            p2 = p.cacheWaifu2xImage
        else:
            p2 = p.cacheImage

        pixMap = QPixmap(p2)
        self.scrollArea.SetPixIem(index, pixMap, waifu2x)

    @time_me
    def ShowOtherPage(self):
        if self.stripModel in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            size = config.PreLook
        elif self.stripModel in [ReadMode.LeftRightDouble, ReadMode.RightLeftDouble]:
            size = 2
        else:
            size = 0

        for index in range(self.curIndex + 1, self.curIndex + size):
            self.ShowPage(index)
        # self.frame.ScalePicture()
        return True

    @time_me
    def ShowImg(self):
        p = self.pictureData.get(self.curIndex)

        if not p or (not p.data) or (not p.cacheImage):
            if not p or (not p.data):
                self.qtTool.SetData(state=QtFileData.Downloading)
            else:
                self.qtTool.SetData(state=QtFileData.Converting)

            self.scrollArea.SetPixIem(self.curIndex, None)

            self.qtTool.modelBox.setEnabled(False)
            self.frame.UpdateProcessBar(None)
            self.frame.process.show()
            return

        self.frame.process.hide()
        if config.CanWaifu2x:
            self.qtTool.modelBox.setEnabled(True)
        assert isinstance(p, QtFileData)
        waifu2x = False
        if not Setting.IsOpenWaifu.value:
            self.frame.waifu2xProcess.hide()
            self.qtTool.SetData(waifuSize=QSize(0, 0), waifuDataLen=0)
            p2 = p.cacheImage

        elif p.cacheWaifu2xImage:
            p2 = p.cacheWaifu2xImage
            waifu2x = True
            self.frame.waifu2xProcess.hide()
            self.qtTool.SetData(waifuSize=p.waifuQSize, waifuDataLen=p.waifuDataSize,
                                waifuTick=p.waifuTick)

        else:
            p2 = p.cacheImage
            if Setting.IsOpenWaifu.value:
                self.frame.waifu2xProcess.show()
            else:
                self.frame.waifu2xProcess.hide()

        self.qtTool.SetData(pSize=p.qSize, dataLen=p.size, state=p.state, waifuState=p.waifuState)
        self.qtTool.UpdateText(p.model)

        pixMap = QPixmap(p2)
        self.scrollArea.SetPixIem(self.curIndex, pixMap, waifu2x)
        # self.graphicsView.setSceneRect(QRectF(QPointF(0, 0), QPointF(pixMap.width(), pixMap.height())))
        # self.frame.ScalePicture()
        self.CheckLoadPicture()
        return True

    def AddHistory(self):
        bookName = QtOwner().bookInfoView.bookName
        url = QtOwner().bookInfoView.url
        path = QtOwner().bookInfoView.path
        QtOwner().historyView.AddHistory(self.bookId, bookName, self.epsId, self.curIndex, url, path)
        return

    def ShowAndCloseTool(self):
        if self.qtTool.isHidden():
            self.qtTool.show()
        else:
            self.qtTool.hide()

    def Waifu2xBack(self, data, waifu2xId, index, tick):
        p = self.pictureData.get(index)
        if waifu2xId <= 0 or not p:
            Log.Error("Not found waifu2xId ：{}, index: {}".format(str(waifu2xId), str(index)))
            return
        p.SetWaifuData(data, round(tick, 2))
        if data:
            self.AddQImageTask(data, self.ConvertQImageWaifu2xBack, index)
        if index == self.curIndex:
            self.qtTool.SetData(waifuState=p.waifuState)
            self.frame.waifu2xProcess.hide()
            # self.ShowImg()
        elif self.stripModel in [ReadMode.UpDown, ReadMode.RightLeftScroll,
                                 ReadMode.LeftRightScroll] and self.curIndex < index <= self.curIndex + config.PreLoading - 1:
            # self.ShowOtherPage()
            self.CheckLoadPicture()
        else:
            self.CheckLoadPicture()

    def ConvertQImageWaifu2xBack(self, data, index):
        assert isinstance(data, QImage)
        p = self.pictureData.get(index)
        if not p:
            return
        assert isinstance(p, QtFileData)
        p.cacheWaifu2xImage = data
        if index == self.curIndex:
            self.ShowImg()
        elif self.stripModel in [ReadMode.UpDown, ReadMode.RightLeftScroll,
                                 ReadMode.LeftRightScroll] and self.curIndex < index <= self.curIndex + config.PreLoading - 1:
            self.ShowOtherPage()
        elif self.stripModel in [ReadMode.RightLeftDouble,
                                 ReadMode.LeftRightDouble] and self.curIndex < index <= self.curIndex + 1:
            self.ShowOtherPage()
        return

    def AddCovertData(self, i):
        info = self.pictureData[i]
        if not info and info.data:
            return
        assert isinstance(info, QtFileData)
        path = ToolUtil.GetRealPath(i + 1, "book/{}/{}".format(self.bookId, self.epsId + 1))
        info.waifu2xTaskId = self.AddConvertTask(path, info.data, info.model, self.Waifu2xBack, i)
        if i == self.curIndex:
            self.qtTool.SetData(waifuState=info.waifuState)
            self.frame.waifu2xProcess.show()

    def InitDownload(self):
        self.AddDownloadBook(self.bookId, self.epsId, 0, statusBack=self.StartLoadPicUrlBack, backParam=0, isInit=True)

    def AddDownload(self, i):
        loadPath = QtOwner().downloadView.GetDownloadFilePath(self.bookId, self.epsId, i)
        self.AddDownloadBook(self.bookId, self.epsId, i,
                             downloadCallBack=self.UpdateProcessBar,
                             completeCallBack=self.CompleteDownloadPic,
                             backParam=i, loadPath=loadPath)
        if i not in self.pictureData:
            data = QtFileData()
            self.pictureData[i] = data
        self.qtTool.SetData(state=self.pictureData[i].state)

    def ChangeReadMode(self, index):
        self.qtTool.comboBox.setCurrentIndex(index)
