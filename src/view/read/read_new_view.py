from __future__ import annotations
from typing import TYPE_CHECKING

from view.read.read_new_frame import ReadNewFrame
from view.read.read_new_graphics import ReadNewGraphics
from view.read.read_new_task import ReadNewTask
from view.read.read_new_tool import ReadNewTool

if TYPE_CHECKING:
    from view.read.read_graphics import ReadGraphicsView

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
from view.read.read_enum import ReadMode, QtFileData, ReadShowState
from view.read.read_frame import ReadFrame

# 每个图片预取队列最多同时下载 5 张，避免较大的预取范围占满下载线程和网络连接池。
PICTURE_PREFETCH_CONCURRENCY = 5


class ReadNewView(QtWidgets.QWidget):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.readTask = ReadNewTask(self)

        self.bookId = ""
        self.token = ""
        self.epsId = 0
        self.resetCnt = config.ResetCnt
        self.curIndex = 0

        self.pictureData: dict[int, QtFileData] = {}
        self.maxPic = 0
        # desktop = QGuiApplication.primaryScreen().geometry()
        # self.resize(desktop.width() // 4 * 3, desktop.height() - 100)
        # self.move(desktop.width() // 8, 0)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = ReadNewFrame(self)
        # self.gridLayout.addWidget(self.scrollArea)
        self.gridLayout.addWidget(self.frame)
        self.setMinimumSize(300, 300)
        self.category = []
        self.isInit = False
        self.epsName = ""

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.SelectMenu)
        self.isShowMenu = False

        # self.stripModel = ReadMode(Setting.LookReadMode.value)
        # self.frame.scrollArea.initReadMode = self.stripModel

        # self.ChangeReadMode(Setting.LookReadMode.value)
        self.qtTool.ChangeReadMode2(Setting.LookReadMode.value)
        self.qtTool.turnSpeed.setValue(Setting.TurnSpeed.value / 1000)
        self.qtTool.scrollSpeed.setValue(Setting.ScrollSpeed.value)
        self.qtTool.scrollInitSpeed.setValue(Setting.ScrollInitSpeed.value)
        self.qtTool.scrollTime.setValue(Setting.ScrollTime.value)
        self.pageIndex = -1
        self.isOffline = False
        self.isLocal = False
        self._cacheBook = None
        self.lastPath = ""
        self._prefetchChapter = None
        self._prefetchCount = 0
        self._prefetchNextIndex = 0
        self._prefetchActive = 0
        self._prefetchReady = False
        self._prefetchChapterMax = 0
        # QtOwner().owner.WindowsSizeChange.connect(self.qtTool.ClearQImage)

    @property
    def cacheBook(self):
        if self._cacheBook:
            if self._cacheBook.eps:
                if self.epsId >= 0 and self.epsId < len(self._cacheBook.eps):
                    return self._cacheBook.eps[self.epsId]
        return self._cacheBook

    @property
    def scrollArea(self) -> ReadNewGraphics:
        return self.frame.scrollArea

    def retranslateUi(self, View):
        self.qtTool.retranslateUi(self.qtTool)
        self.qtTool.modelNameButton.setText(ToolUtil.GetShowModelName(Setting.LookModelName.value))
        self.qtTool.modelNameButton.setToolTip(Setting.LookModelName.value)

    def SelectMenu(self):
        popMenu = QMenu(self)
        action = popMenu.addAction(Str.GetStr(Str.Menu) + "(F12)")
        action.triggered.connect(self.ShowAndCloseTool)

        action = popMenu.addAction(Str.GetStr(Str.FullSwitch) + "(F11)")
        action.triggered.connect(self.qtTool.FullScreen)

        if config.CanWaifu2x:
            if Setting.IsOpenWaifu.value:
                action = popMenu.addAction(Str.GetStr(Str.CloseAutoWaifu2x))
            else:
                action = popMenu.addAction(Str.GetStr(Str.OpenAutoWaifu2x))
            action.triggered.connect(self.qtTool.checkBox.click)

        p = self.pictureData.get(self.curIndex)
        if config.CanWaifu2x:
            if p:
                if p.isWaifu2x:
                    action = popMenu.addAction(Str.GetStr(Str.CloseCurWaifu2x) + "(F2)")
                else:
                    action = popMenu.addAction(Str.GetStr(Str.OpenCurWaifu2x) + "(F2)")
                action.triggered.connect(self.qtTool.curWaifu2x.click)

        menu2 = popMenu.addMenu(Str.GetStr(Str.ReadMode))
        action = menu2.addAction(Str.GetStr(Str.ToggleDoublePageAlign) + "(F10)")
        # action.triggered.connect(self.ChangeDoublePage)

        def AddReadMode(name, value):
            action = menu2.addAction(name)
            action.triggered.connect(partial(self.qtTool.ChangeReadMode, value))
            if self.scrollArea._mode.value == value:
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
        AddReadMode(Str.GetStr(Str.RightLeftScroll2), 8)

        menu3 = popMenu.addMenu(Str.GetStr(Str.Scale) + "(- +)")

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

        menu3 = popMenu.addMenu(Str.GetStr(Str.SwitchPage) + "(← →)")
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

        # action = popMenu.addAction(Str.GetStr(Str.AutoScroll) + "(F5)")
        # action.triggered.connect(self.qtTool.SwitchScrollAndTurn)

        action = popMenu.addAction(Str.GetStr(Str.Exit) + "(Esc)")
        action.triggered.connect(self.Close)

        if self.qtTool.IsStartScrollAndTurn():
            action.setCheckable(True)
            action.setChecked(True)

        self.isShowMenu = True
        popMenu.exec_(QCursor.pos())

    @property
    def qtTool(self) -> ReadNewTool:
        return self.frame.qtTool

    def Close(self):
        self.ReturnPage()
        # self.frame.scrollArea.ClearPixItem()
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
        Setting.ScrollInitSpeed.SetValue(int(self.qtTool.scrollInitSpeed.value()))
        Setting.ScrollTime.SetValue(int(self.qtTool.scrollTime.value()))
        self.qtTool.UpdateText("")
        self.frame.UpdateProcessBar(None)
        self.frame.UpdateProcessBar2(None)
        # self.qtTool.CloseScrollAndTurn()
        self.bookId = ""
        self.epsId = 0
        self.maxPic = 0
        self.curIndex = 0
        self.frame.oldValue = 0
        self.pictureData.clear()
        self._prefetchChapter = None
        self._prefetchCount = 0
        self._prefetchNextIndex = 0
        self._prefetchActive = 0
        self._prefetchReady = False
        self._prefetchChapterMax = 0
        QtOwner().SetSubTitle("")
        self.readTask.ClearTask()
        self.readTask.ClearDownload()
        self.readTask.ClearQImageTask()

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

    def StartLoadPicUrlBack(self, raw, v):
        st = raw["st"]
        QtOwner().CloseLoading()
        if st == Status.Error or st == Str.SpaceEps:
            QtOwner().ShowError(Str.GetStr(st))
            return

        maxPic = raw.get("maxPic")
        if not maxPic or self.maxPic > 0:
            return
        self.maxPic = maxPic
        title = raw.get("title", "")
        self.epsName = title
        self.AddHistory()
        self.scrollArea.init_all_image(self.maxPic, self.curIndex)
        self.qtTool.UpdateSlider()
        self.qtTool.InitSlider(self.maxPic)
        return

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
            url = QtOwner().bookInfoView.GetBookUrl()
            path = QtOwner().bookInfoView.GetBookUrlPath()
            QtOwner().historyView.AddHistory(self.bookId, bookName, self.epsId, self.curIndex, url, path)
        return

    def ShowAndCloseTool(self):
        if self.qtTool.isHidden():
            self.qtTool.show()
        else:
            self.qtTool.hide()

    def InitDownload(self):
        if self.isLocal:
            assert isinstance(self.cacheBook, LocalData)
            raw = {"st": Status.Ok, "maxPic": self.cacheBook.picCnt, "title": self.cacheBook.title}
            self.StartLoadPicUrlBack(raw, "")
        elif not self.isOffline:
            self.readTask.AddDownloadBook(self.bookId, self.epsId, 0, statusBack=self.StartLoadPicUrlBack, backParam=0,
                                 isInit=True)
        else:
            bookInfo = BookMgr().GetBook(self.bookId)
            downInfo = QtOwner().downloadView.GetDownloadEpsInfo(self.bookId, self.epsId)
            if not bookInfo or not downInfo:
                QtOwner().ShowError(Str.GetStr(Str.FileError))
            else:
                assert isinstance(downInfo, DownloadEpsItem)
                raw = {"st": Status.Ok, "maxPic": downInfo.picCnt, "title": downInfo.epsTitle}
                self.StartLoadPicUrlBack(raw, "")

    def CopyFile(self):
        info = self.pictureData.get(self.curIndex)
        if not info:
            return
        assert isinstance(info, QtFileData)
        if not info.data and not info.waifuData:
            return

        # today = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        if info.waifuData:
            _, _, mat, _ = ToolUtil.GetPictureSize(info.waifuData)
            path = "{}_{}_waifu2x.{}".format(self.bookId, self.curIndex + 1, mat)
            data = info.waifuData
        else:
            _, _, mat, _ = ToolUtil.GetPictureSize(info.data)
            path = "{}_{}.{}".format(self.bookId, self.curIndex + 1, mat)
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
            _, _, mat, _ = ToolUtil.GetPictureSize(info.waifuData)
            path = "{}_{}_waifu2x.{}".format(self.bookId, self.curIndex + 1, mat)
            data = info.waifuData
        else:
            _, _, mat, _ = ToolUtil.GetPictureSize(info.data)
            path = "{}_{}.{}".format(self.bookId, self.curIndex + 1, mat)
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