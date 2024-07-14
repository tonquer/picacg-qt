import os
import time
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize, QEvent, QMimeData
from PySide6.QtGui import QPixmap, QImage, QCursor
from PySide6.QtWidgets import QMenu, QApplication, QFileDialog

from config import config
from config.setting import Setting
from qt_owner import QtOwner
from server import req, Status, Log
from task.qt_task import QtTaskBase
from task.task_local import LocalData
from tools.book import BookMgr
from tools.str import Str
from tools.tool import time_me, ToolUtil
from view.download.download_item import DownloadItem, DownloadEpsItem
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
        self.frame.scrollArea.initReadMode = self.stripModel

        self.ChangeReadMode(Setting.LookReadMode.value)
        self.qtTool.ChangeReadMode2(Setting.LookReadMode.value)
        self.qtTool.turnSpeed.setValue(Setting.TurnSpeed.value / 1000)
        self.qtTool.scrollSpeed.setValue(Setting.ScrollSpeed.value)
        self.pageIndex = -1
        self.isOffline = False
        self.isLocal = False
        self._cacheBook = None
        self.lastPath = ""
        # QtOwner().owner.WindowsSizeChange.connect(self.qtTool.ClearQImage)

    @property
    def cacheBook(self):
        if self._cacheBook:
            if self._cacheBook.eps:
                if self.epsId >= 0 and self.epsId < len(self._cacheBook.eps):
                    return self._cacheBook.eps[self.epsId]
        return self._cacheBook

    @property
    def scrollArea(self):
        return self.frame.scrollArea

    def retranslateUi(self, View):
        self.qtTool.retranslateUi(self.qtTool)

    def SelectMenu(self):
        popMenu = QMenu(self)
        action = popMenu.addAction(Str.GetStr(Str.Menu)+"(F12)")
        action.triggered.connect(self.ShowAndCloseTool)

        action = popMenu.addAction(Str.GetStr(Str.FullSwitch)+"(F11)")
        action.triggered.connect(self.qtTool.FullScreen)

        if Setting.IsOpenWaifu.value:
            action = popMenu.addAction(Str.GetStr(Str.CloseAutoWaifu2x))
        else:
            action = popMenu.addAction(Str.GetStr(Str.OpenAutoWaifu2x))
        action.triggered.connect(self.qtTool.checkBox.click)

        p = self.pictureData.get(self.curIndex)
        if p:
            if p.isWaifu2x:
                action = popMenu.addAction(Str.GetStr(Str.CloseCurWaifu2x)+"(F2)")
            else:
                action = popMenu.addAction(Str.GetStr(Str.OpenCurWaifu2x)+"(F2)")
            action.triggered.connect(self.qtTool.curWaifu2x.click)

        menu2 = popMenu.addMenu(Str.GetStr(Str.ReadMode))
        action = menu2.addAction("切换双页对齐(F10)")
        action.triggered.connect(self.ChangeDoublePage)

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
        AddReadMode(Str.GetStr(Str.RightLeftDouble2), 6)
        AddReadMode(Str.GetStr(Str.SameWight), 7)

        menu3 = popMenu.addMenu(Str.GetStr(Str.Scale)+ "(- +)")

        def AddScaleMode(name, value):
            action = menu3.addAction(name)
            action.triggered.connect(partial(self.qtTool.ScalePicture2, value))
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

        menu3 = popMenu.addMenu(Str.GetStr(Str.SwitchPage)+"(← →)")
        action = menu3.addAction(Str.GetStr(Str.LastChapter))
        action.triggered.connect(self.qtTool.OpenLastEps)
        action = menu3.addAction(Str.GetStr(Str.NextChapter))
        action.triggered.connect(self.qtTool.OpenNextEps)

        menu4 = popMenu.addMenu(Str.GetStr(Str.Copy))
        action = menu4.addAction(Str.GetStr(Str.CopyPicture) + "(F1)")
        action.triggered.connect(self.CopyPicture)

        action = menu4.addAction(Str.GetStr(Str.CopyFile) + "(F3)")
        action.triggered.connect(self.CopyFile)

        action = menu4.addAction(Str.GetStr(Str.CopyFileLast) + "(F4)")
        action.triggered.connect(self.CopyLastFile)

        action = popMenu.addAction(Str.GetStr(Str.AutoScroll)+"(F5)")
        action.triggered.connect(self.qtTool.SwitchScrollAndTurn)

        action = popMenu.addAction(Str.GetStr(Str.Exit) + "(Esc)")
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

    def Stop(self):
        self.frame.process.timer.stop()
        self.frame.process2.timer.stop()

    def Clear(self):
        Setting.TurnSpeed.SetValue(int(self.qtTool.turnSpeed.value() * 1000))
        Setting.ScrollSpeed.SetValue(int(self.qtTool.scrollSpeed.value()))
        self.qtTool.UpdateText("")
        self.frame.UpdateProcessBar(None)
        self.frame.UpdateProcessBar2(None)
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

    def OpenPage(self, bookId, epsId, pageIndex=-1, isOffline=False):
        if not bookId:
            return
        self.isOffline = isOffline
        self.isLocal = False
        self._cacheBook = None
        self.Clear()
        info = BookMgr().GetBook(bookId)
        if info:
            self.category = info.categories[::]

        self.qtTool.checkBox.setChecked(Setting.IsOpenWaifu.value)
        self.qtTool.preDownWaifu2x.setChecked(Setting.PreDownWaifu2x.value)
        self.qtTool.curWaifu2x.setChecked(Setting.IsOpenWaifu.value)
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

        QtOwner().ShowLoading()

        # 开始加载
        self.InitDownload()

        if config.IsTips:
            config.IsTips = 0
            self.frame.InitHelp()

    def OpenLocalPage(self, v, epsId=0, pageIndex=-1):
        if not v:
            return
        self.Clear()
        assert isinstance(v, LocalData)
        self.epsId = epsId
        self._cacheBook = v
        self.pageIndex = self.cacheBook.lastIndex
        if pageIndex >= 0:
           self.pageIndex = pageIndex

        self.isOffline = False
        self.isLocal = True

        self.qtTool.checkBox.setChecked(Setting.IsOpenWaifu.value)
        self.qtTool.preDownWaifu2x.setChecked(Setting.PreDownWaifu2x.value)
        self.qtTool.curWaifu2x.setChecked(Setting.IsOpenWaifu.value)
        self.qtTool.SetData(isInit=True)
        self.qtTool.SetData()

        # self.qtTool.show()
        self.bookId = self.cacheBook.id

        self.qtTool.isMaxFull = self.window().isMaximized()
        if Setting.LookReadFull.value:
            QtOwner().owner.showFullScreen()
            self.qtTool.fullButton.setText(Str.GetStr(Str.ExitFullScreen))

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

    def GetIsWaifu2x(self):
        p = self.pictureData.get(self.curIndex)
        if not p:
            return Setting.IsOpenWaifu.value
        return p.isWaifu2x

    def SetIsWaifu2x(self, isWaifu2x):
        p = self.pictureData.get(self.curIndex)
        if not p:
            return
        p.isWaifu2x = isWaifu2x
        if isWaifu2x and (p.waifuState == p.OverResolution or p.waifuState == p.AnimationNotAuto):
            p.waifuState = p.WaifuStateCancle
        if ReadMode.isDouble(self.stripModel):
            p = self.pictureData.get(self.curIndex+1)
            if not p:
                return
            p.isWaifu2x = isWaifu2x

    def CheckLoadPicture(self):
        # i = 0
        newDict = {}
        needUp = False
        removeTaskIds = []

        if not self.maxPic:
            return

        preLoadList = list(range(self.curIndex, self.curIndex + config.PreLoading))
        preQImage = list(range(self.curIndex, self.curIndex + config.PreLook))

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
            p = self.pictureData.get(i)
            if not p or not p.data:
                break
            if not p.isWaifu2x:
                continue
            if p.waifuState == p.WaifuStateCancle or p.waifuState == p.WaifuWait:
                p.waifuState = p.WaifuStateStart
                self.AddCovertData(i)
                break
            if p.waifuState == p.WaifuStateStart:
                break

        for i in preQImage:
            p = self.pictureData.get(i)
            if not p or not p.data:
                continue
            assert isinstance(p, QtFileData)
            if not (p.cacheImage or p.cacheImageTaskId > 0):
                self.CheckToQImage(i, p, False)

            if not (not p.waifuData or p.cacheWaifu2xImage or p.cacheWaifu2xImageTaskId > 0):
                self.CheckToQImage(i, p, True)

        for i in set(self.pictureData.keys()) - set(preQImage):
            p = self.pictureData.get(i)
            if not p:
                continue
            assert isinstance(p, QtFileData)
            if p.cacheImageTaskId > 0:
                self.ClearQImageTaskById(p.cacheImageTaskId)
                p.cacheImageTaskId = 0
            if p.cacheWaifu2xImageTaskId > 0:
                self.ClearQImageTaskById(p.cacheWaifu2xImageTaskId)
                p.cacheWaifu2xImageTaskId = 0
            p.cacheImage = None
            p.cacheWaifu2xImage = None
        pass

    def StartLoadPicUrlBack(self, raw, v):
        st = raw["st"]
        if st == Status.Error or st == Str.SpaceEps:
            QtOwner().ShowError(Str.GetStr(st))
            return

        maxPic = raw.get("maxPic")
        if not maxPic or self.maxPic > 0:
            return
        self.maxPic = maxPic
        title = raw.get("title", "")
        self.epsName = title
        # info = BookMgr().GetBook(self.bookId)

        if 0 < self.pageIndex < self.maxPic:
            self.curIndex = self.pageIndex
            QtOwner().ShowMsg(Str.GetStr(Str.ContinueRead) + str(self.pageIndex + 1) + Str.GetStr(Str.Page))
        elif self.pageIndex > self.maxPic:
            self.curIndex = self.maxPic-1
            # QtOwner().ShowMsg(Str.GetStr(Str.ContinueRead) + str(self.maxPic) + Str.GetStr(Str.Page))

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
        if ReadMode.isDouble(self.stripModel):
            if self.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftDouble2]:
                if backParam == self.curIndex:
                    self.frame.UpdateProcessBar(info)
                elif backParam == self.curIndex + 1:
                    self.frame.UpdateProcessBar2(info)
            else:
                if backParam == self.curIndex:
                    self.frame.UpdateProcessBar2(info)
                elif backParam == self.curIndex + 1:
                    self.frame.UpdateProcessBar(info)
        else:
            if self.curIndex == backParam:
                self.frame.UpdateProcessBar(info)

    def CompleteDownloadPic(self, data, st, index):
        QtOwner().CloseLoading()
        p = self.pictureData.get(index)
        if not p:
            p = QtFileData()
            self.pictureData[index] = p
        if st == Status.FileError:
            QtOwner().ShowError(Str.GetStr(st))
        elif st != Status.Ok:
            p.state = p.DownloadReset
            if QtOwner().owner.totalStackWidget.currentIndex == 0:
                return
            self.AddDownload(index)
        else:
            p.SetData(data, self.category)
            # self.CheckToQImage()
            self.CheckLoadPicture()
        self.CheckSetProcess()

    def CheckToQImage(self, index, p, isWaifu2x=False):
        assert isinstance(p, QtFileData)
        model = self.qtTool.stripModel
        toW, toH = QtFileData.GetReadScale(self.qtTool.stripModel, 0, self.scrollArea.width(),
                                           self.scrollArea.height(), True)
        if not isWaifu2x:
            if p.data:
                p.cacheImage = None
                p.cacheImageScale = self.frame.scaleCnt
                p.cacheImageTaskId = self.AddQImageTask(p.data, self.devicePixelRatio(), toW, toH, model, self.ConvertQImageBack, index)
        else:
            if p.waifuData:
                p.cacheWaifu2xImage = None
                p.cacheWaifu2xImageScale = self.frame.scaleCnt
                p.cacheImageWaifu2xTaskId = self.AddQImageTask(p.waifuData, self.devicePixelRatio(), toW, toH, model, self.ConvertQImageWaifu2xBack, index)

    def ConvertQImageBack(self, data, index):
        assert isinstance(data, QImage)
        p = self.pictureData.get(index)
        if not p:
            return
        assert isinstance(p, QtFileData)
        p.cacheImage = data
        p.cacheImageTaskId = 0
        if index == self.curIndex:
            self.ShowImg(index)
        elif self.stripModel in [ReadMode.UpDown, ReadMode.RightLeftScroll,
                                 ReadMode.LeftRightScroll] and self.curIndex < index <= self.curIndex + config.PreLoading - 1:
            self.ShowImg(index)
        elif ReadMode.isDouble(self.stripModel) and self.curIndex < index <= self.curIndex + 1:
            self.ShowImg(index)
        self.CheckSetWaifu2xProcess()
        return

    # def ShowPage(self, index):
    #     if index >= self.maxPic:
    #         return
    #
    #     p = self.pictureData.get(index)
    #     if not p or (not p.data) or (not p.cacheImage):
    #         self.scrollArea.SetPixIem(index, None)
    #         return
    #
    #     waifu2x = False
    #     assert isinstance(p, QtFileData)
    #
    #     if not p.isWaifu2x:
    #         p2 = p.cacheImage
    #
    #     elif p.cacheWaifu2xImage:
    #         waifu2x = True
    #         p2 = p.cacheWaifu2xImage
    #     else:
    #         p2 = p.cacheImage
    #
    #     if p.isGif and not ReadMode.isScroll(self.stripModel):
    #         self.scrollArea.SetGifData(index, p.data, p.w, p.h)
    #         w, h = p2.wight(), p2.heigh()
    #         if p.waifuData:
    #             self.scrollArea.SetGifData(index, p.waifuData, w, h)
    #         else:
    #             self.scrollArea.SetGifData(index, p.data, w, h)
    #     else:
    #         pixMap = QPixmap(p2)
    #         self.scrollArea.SetPixIem(index, pixMap, waifu2x)

    # @time_me
    # def ShowOtherPage(self):
    #     if self.stripModel in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
    #         size = config.PreLook
    #     elif ReadMode.isDouble(self.stripModel):
    #         size = 2
    #     else:
    #         size = 0
    #
    #     for index in range(self.curIndex + 1, self.curIndex + size):
    #         self.ShowPage(index)
    #     # self.frame.ScalePicture()
    #     return True

    def ShowImgAll(self):
        if self.stripModel in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            size = config.PreLook
        elif ReadMode.isDouble(self.stripModel):
            size = 2
        else:
            size = 1

        for index in range(self.curIndex, self.curIndex + size):
            self.ShowImg(index)
        self.CheckSetProcess()
        self.CheckSetWaifu2xProcess()
        self.CheckLoadPicture()

    @time_me
    def ShowImg(self, index):
        if index >= self.maxPic:
            return
        isCurIndex = index == self.curIndex
        p = self.pictureData.get(index)
        if not p or (not p.data) or (not p.cacheImage):
            self.scrollArea.SetPixIem(index, None)
            if isCurIndex:
                if not p or (not p.data):
                    self.qtTool.SetData(state=QtFileData.Downloading)
                else:
                    self.qtTool.SetData(state=QtFileData.Converting)

                self.qtTool.modelBox.setEnabled(False)
                # self.frame.process.show()
            return
        if isCurIndex:
            # self.frame.process.hide()
            if config.CanWaifu2x:
                self.qtTool.modelBox.setEnabled(True)

        assert isinstance(p, QtFileData)
        waifu2x = False
        if not p.isWaifu2x:
            if isCurIndex:
                # self.frame.waifu2xProcess.hide()
                self.qtTool.SetData(waifuSize=QSize(0, 0), waifuDataLen=0)

            p2 = p.cacheImage

        elif p.cacheWaifu2xImage:
            p2 = p.cacheWaifu2xImage
            waifu2x = True
            if isCurIndex:
                # self.frame.waifu2xProcess.hide()
                self.qtTool.SetData(waifuSize=p.waifuQSize, waifuDataLen=p.waifuDataSize,
                                    waifuTick=p.waifuTick)

        else:
            p2 = p.cacheImage
            # if isCurIndex:
            #     if p.isWaifu2x:
            #         self.frame.waifu2xProcess.show()
            #     else:
            #         self.frame.waifu2xProcess.hide()

        if isCurIndex:
            self.qtTool.SetData(pSize=p.qSize, dataLen=p.size, state=p.state, waifuState=p.waifuState)
            self.qtTool.UpdateText(p.model)

        if self.frame.scrollArea.IsAlreadLoad(index, waifu2x):
            # print("already load, {}".format(index))
            return

        if p.isGif and not ReadMode.isScroll(self.stripModel):
            if p.isWaifu2x and p.waifuData:
                self.scrollArea.SetGifData(index, p.waifuData, p2, True)
            else:
                self.scrollArea.SetGifData(index, p.data, p2)
        else:
            pixMap = QPixmap(p2)
            pixMap.setDevicePixelRatio(p2.devicePixelRatio())
            # print("set index 1, {}".format(index))
            self.scrollArea.SetPixIem(index, pixMap, waifu2x)
        # self.graphicsView.setSceneRect(QRectF(QPointF(0, 0), QPointF(pixMap.width(), pixMap.height())))
        # self.frame.ScalePicture()
        return True

    def CheckClearProcess(self):
        self.frame.UpdateProcessBar(None)
        self.frame.UpdateProcessBar2(None)

    def CheckSetProcess(self):
        if not ReadMode.isDouble(self.stripModel):
            self.frame.process2.hide()
            index = self.curIndex
            p = self.pictureData.get(index)

            if not p or (not p.data):
                self.frame.process.show()
            else:
                self.frame.process.hide()

        elif self.stripModel not in [ReadMode.RightLeftDouble, ReadMode.RightLeftDouble2]:
            index = self.curIndex
            p = self.pictureData.get(index)
            if not p or (not p.data):
                self.frame.process2.show()
            else:
                self.frame.process2.hide()

            index = self.curIndex+1
            if index >= self.maxPic:
                self.frame.process.hide()
                return
            p = self.pictureData.get(index)
            if not p or (not p.data):
                self.frame.process.show()
            else:
                self.frame.process.hide()
        else:
            index = self.curIndex
            p = self.pictureData.get(index)
            if not p or (not p.data):
                self.frame.process.show()
            else:
                self.frame.process.hide()

            index = self.curIndex+1
            if index >= self.maxPic:
                self.frame.process2.hide()
                return
            p = self.pictureData.get(index)
            if not p or (not p.data):
                self.frame.process2.show()
            else:
                self.frame.process2.hide()

    def CheckSetWaifu2xProcess(self):
        if not ReadMode.isDouble(self.stripModel):
            self.frame.waifu2xProcess2.hide()
            index = self.curIndex
            p = self.pictureData.get(index)
            if not p:
                self.frame.waifu2xProcess.hide()
                return
            if p.isWaifu2x and not p.cacheWaifu2xImage:
                self.frame.waifu2xProcess.show()
            else:
                self.frame.waifu2xProcess.hide()
        elif self.stripModel not in [ReadMode.RightLeftDouble, ReadMode.RightLeftDouble2]:
            index = self.curIndex
            p = self.pictureData.get(index)
            if not p:
                self.frame.waifu2xProcess2.hide()
                return
            if p.isWaifu2x and not p.cacheWaifu2xImage:
                self.frame.waifu2xProcess2.show()
            else:
                self.frame.waifu2xProcess2.hide()

            index = self.curIndex+1
            if index >= self.maxPic:
                self.frame.waifu2xProcess.hide()
                return
            p = self.pictureData.get(index)
            if not p:
                self.frame.waifu2xProcess.hide()
                return
            if p.isWaifu2x and not p.cacheWaifu2xImage:
                self.frame.waifu2xProcess.show()
            else:
                self.frame.waifu2xProcess.hide()
        else:
            index = self.curIndex
            p = self.pictureData.get(index)
            if not p:
                self.frame.waifu2xProcess.hide()
                return
            if p.isWaifu2x and not p.cacheWaifu2xImage:
                self.frame.waifu2xProcess.show()
            else:
                self.frame.waifu2xProcess.hide()

            index = self.curIndex+1
            if index >= self.maxPic:
                self.frame.waifu2xProcess2.hide()
                return
            p = self.pictureData.get(index)
            if not p:
                self.frame.waifu2xProcess2.hide()
                return
            if p.isWaifu2x and not p.cacheWaifu2xImage:
                self.frame.waifu2xProcess2.show()
            else:
                self.frame.waifu2xProcess2.hide()

    def AddHistory(self):
        if self.isLocal:
            assert isinstance(self.cacheBook, LocalData)
            self.cacheBook.lastIndex = self.curIndex
            self.cacheBook.lastReadTime = int(time.time())
            if self._cacheBook.eps:
                self._cacheBook.lastReadTime = int(time.time())
                QtOwner().localReadView.UpdateLastTick(self._cacheBook.id)
                QtOwner().localReadView.AddEpsDataToDB(self._cacheBook.id, self.cacheBook.id)
            else:
                QtOwner().localReadView.AddDataToDB(self.cacheBook.id)
        else:
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
            model = self.qtTool.stripModel
            self.CheckLoadPicture()
            # self.CheckToQImage(index, p, True)
            # toW, toH = QtFileData.GetReadScale(self.qtTool.stripModel, self.frame.scaleCnt, self.scrollArea.width(), self.scrollArea.height())
            # self.AddQImageTask(data, self.devicePixelRatio(), toW, toH, model, self.ConvertQImageWaifu2xBack, index)
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
        p.cacheWaifu2xImageTaskId = 0
        if index == self.curIndex:
            self.ShowImg(index)
        elif self.stripModel in [ReadMode.UpDown, ReadMode.RightLeftScroll,
                                 ReadMode.LeftRightScroll] and self.curIndex < index <= self.curIndex + config.PreLoading - 1:
            self.ShowImg(index)
        elif ReadMode.isDouble(self.stripModel) and self.curIndex < index <= self.curIndex + 1:
            self.ShowImg(index)
        self.CheckSetWaifu2xProcess()
        return

    def AddCovertData(self, i):
        info = self.pictureData[i]
        if not info and info.data:
            return
        assert isinstance(info, QtFileData)
        path = ToolUtil.GetRealPath(i + 1, "book/{}/{}".format(self.bookId, self.epsId + 1))
        if Setting.PreDownWaifu2x.value:
            filePath = QtOwner().downloadView.GetDownloadWaifu2xFilePath(self.bookId, self.epsId, i)
        else:
            filePath = ""
        if self.isLocal:
            info.waifu2xTaskId = self.AddConvertTask(path, info.data, info.model, self.Waifu2xBack, i, noSaveCache=True)
        else:
            info.waifu2xTaskId = self.AddConvertTask(path, info.data, info.model, self.Waifu2xBack, i,
                                                     preDownPath=filePath)
        if i == self.curIndex:
            self.qtTool.SetData(waifuState=info.waifuState)
            self.frame.waifu2xProcess.show()

    def InitDownload(self):
        if self.isLocal:
            assert isinstance(self.cacheBook, LocalData)
            raw = {"st": Status.Ok, "maxPic": self.cacheBook.picCnt, "title": self.cacheBook.title}
            self.StartLoadPicUrlBack(raw, "")
        elif not self.isOffline:
            self.AddDownloadBook(self.bookId, self.epsId, 0, statusBack=self.StartLoadPicUrlBack, backParam=0, isInit=True)
        else:
            bookInfo = BookMgr().GetBook(self.bookId)
            downInfo = QtOwner().downloadView.GetDownloadEpsInfo(self.bookId, self.epsId)
            if not bookInfo or not downInfo:
                QtOwner().ShowError(Str.GetStr(Str.FileError))
            else:
                assert isinstance(downInfo, DownloadEpsItem)
                raw = {"st": Status.Ok, "maxPic": downInfo.picCnt, "title": downInfo.epsTitle}
                self.StartLoadPicUrlBack(raw, "")

    def AddDownload(self, i):
        loadPath = QtOwner().downloadView.GetDownloadFilePath(self.bookId, self.epsId, i)
        if self.isLocal:
            assert isinstance(self.cacheBook, LocalData)
            self.AddLocalTaskLoadPicture(self.cacheBook, i, callBack=self.CompleteDownloadPic, backparam=i)
        elif not self.isOffline:
            self.AddDownloadBook(self.bookId, self.epsId, i,
                                 downloadCallBack=self.UpdateProcessBar,
                                 completeCallBack=self.CompleteDownloadPic,
                                 backParam=i, loadPath=loadPath)
        else:
            self.AddDownloadBookCache(loadPath, completeCallBack=self.CompleteDownloadPic, backParam=i)
        if i not in self.pictureData:
            data = QtFileData()
            self.pictureData[i] = data
        if i == self.curIndex:
            self.qtTool.SetData(state=self.pictureData[i].state)
        # self.CheckClearProcess(i)
        self.CheckSetProcess()

    def ChangeReadMode(self, index):
        self.qtTool.comboBox.setCurrentIndex(index)

    def ChangeDoublePage(self):
        if not ReadMode.isDouble(self.stripModel):
            return
        if self.curIndex < self.maxPic:
            self.curIndex += 1
        self.frame.oldValue = 0
        self.qtTool.SetData(isInit=True)
        self.scrollArea.ResetScrollValue(self.curIndex)
        self.scrollArea.changeNextPage.emit(self.curIndex)

    def CopyFile(self):
        info = self.pictureData.get(self.curIndex)
        if not info:
            return
        assert isinstance(info, QtFileData)
        if not info.data and not info.waifuData:
            return

        # today = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        if info.waifuData:
            path = "{}_{}_waifu2x.jpg".format(self.bookId, self.curIndex+1)
            data = info.waifuData
        else:
            path = "{}_{}.jpg".format(self.bookId, self.curIndex+1)
            data = info.data
        if not data:
            return
        try:
            if self.lastPath:
                path = os.path.join(self.lastPath, path)
            filepath = QFileDialog.getSaveFileName(self, Str.GetStr(Str.Save), path, "Image Files(*.jpg *.png)")
            if filepath and len(filepath) >= 1:
                name = filepath[0]
                if not name:
                    return
                self.lastPath = os.path.dirname(name)
                f = open(name, "wb")
                f.write(data)
                f.close()
                QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        except Exception as es:
            Log.Error(es)

    def CopyLastFile(self):
        info = self.pictureData.get(self.curIndex)
        if not info:
            return
        assert isinstance(info, QtFileData)
        if not info.data and not info.waifuData:
            return

        if info.waifuData:
            path = "{}_{}_waifu2x.jpg".format(self.bookId, self.curIndex+1)
            data = info.waifuData
        else:
            path = "{}_{}.jpg".format(self.bookId, self.curIndex+1)
            data = info.data
        if not data:
            return
        try:
            if self.lastPath:
                name = os.path.join(self.lastPath, path)
            else:
                if self.lastPath:
                    path = os.path.join(self.lastPath, path)
                filepath = QFileDialog.getSaveFileName(self, Str.GetStr(Str.Save), path, "Image Files(*.jpg *.png)")
                if filepath and len(filepath) >= 1:
                    name = filepath[0]
                    if not name:
                        return
                    self.lastPath = os.path.dirname(name)
                else:
                    return

            # self.lastPath = os.path.dirname(name)
            f = open(name, "wb")
            f.write(data)
            f.close()
            QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        except Exception as es:
            Log.Error(es)

    def CopyPicture(self):
        info = self.pictureData.get(self.curIndex)
        if not info:
            return
        assert isinstance(info, QtFileData)
        if not info.data and not info.waifuData:
            return
        if info.waifuData:
            data = info.waifuData
        else:
            data = info.data
        p = QImage()
        p.loadFromData(data)

        clipboard = QApplication.clipboard()
        clipboard.setImage(p)
        QtOwner().ShowMsg(Str.GetStr(Str.CopySuc))
        return