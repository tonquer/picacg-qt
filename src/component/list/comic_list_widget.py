from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QListWidgetItem, QMenu, QApplication

from component.list.base_list_widget import BaseListWidget
from component.widget.comic_item_widget import ComicItemWidget
from config import config
from config.setting import Setting
from qt_owner import QtOwner
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class ComicListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.resize(800, 600)
        # self.setMinimumHeight(400)
        self.setFrameShape(self.NoFrame)  # 无边框
        self.setFlow(self.LeftToRight)  # 从左到右
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.SelectMenuBook)
        # self.doubleClicked.connect(self.OpenBookInfo)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.itemClicked.connect(self.SelectItem)
        self.isDelMenu = False
        self.isGame = False

    def SelectMenuBook(self, pos):
        index = self.indexAt(pos)
        widget = self.indexWidget(index)
        if index.isValid() and widget:
            assert isinstance(widget, ComicItemWidget)
            popMenu = QMenu(self)
            action = popMenu.addAction(Str.GetStr(Str.Open))
            action.triggered.connect(partial(self.OpenBookInfoHandler, index))
            action = popMenu.addAction(Str.GetStr(Str.LookCover))
            action.triggered.connect(partial(self.OpenPicture, index))
            action = popMenu.addAction(Str.GetStr(Str.ReDownloadCover))
            action.triggered.connect(partial(self.ReDownloadPicture, index))
            if config.CanWaifu2x and widget.picData:
                if not widget.isWaifu2x:
                    action = popMenu.addAction(Str.GetStr(Str.Waifu2xConvert))
                    action.triggered.connect(partial(self.Waifu2xPicture, index))
                    if widget.isWaifu2xLoading or not config.CanWaifu2x:
                        action.setEnabled(False)
                else:
                    action = popMenu.addAction(Str.GetStr(Str.DelWaifu2xConvert))
                    action.triggered.connect(partial(self.CancleWaifu2xPicture, index))
            action = popMenu.addAction(Str.GetStr(Str.CopyTitle))
            action.triggered.connect(partial(self.CopyHandler, index))
            action = popMenu.addAction(Str.GetStr(Str.Download))
            action.triggered.connect(partial(self.DownloadHandler, index))
            if self.isDelMenu:
                action = popMenu.addAction(Str.GetStr(Str.Delete))
                action.triggered.connect(partial(self.DelHandler, index))
            popMenu.exec_(QCursor.pos())
        return

    def AddBookByDict(self, v):
        _id = v.get("_id")
        title = v.get("title")
        categories = v.get("categories", [])
        if "thumb" in v:
            url = v.get("thumb", {}).get("fileServer")
            path = v.get("thumb", {}).get("path")
        elif "icon" in v:
            url = v.get("icon", {}).get("fileServer")
            path = v.get("icon", {}).get("path")
        else:
            url = ""
            path = ""
        categoryStr = "，".join(categories)
        likesCount = str(v.get("totalLikes", ""))
        finished = v.get("finished")
        pagesCount = v.get("pagesCount")
        self.AddBookItem(_id, title, categoryStr, url, path, likesCount, "", pagesCount, finished)

    def AddBookItemByBook(self, v, isShowHistory=False):
        title = v.title
        url = v.fileServer
        path = v.path
        _id = v.id
        finished = v.finished
        pagesCount = v.pages
        likesCount = str(v.likesCount)
        updated_at = v.updated_at
        categories = v.categories
        updated_at = v.updated_at
        if isShowHistory:
            info = QtOwner().owner.historyView.GetHistory(_id)
            if info:
                categories = Str.GetStr(Str.LastLook) + str(info.epsId + 1) + Str.GetStr(Str.Chapter) + "/" + str(v.epsCount) + Str.GetStr(Str.Chapter)
        self.AddBookItem(_id, title, categories, url, path, likesCount, updated_at, pagesCount, finished)

    def AddBookItemByHistory(self, v):
        _id = v.bookId
        title = v.name
        path = v.path
        url = v.url
        categories = "{} {}".format(ToolUtil.GetUpdateStrByTick(v.tick), Str.GetStr(Str.Looked))
        self.AddBookItem(_id, title, categories, url, path)

    def AddBookItem(self, _id, title, categoryStr="", url="", path="", likesCount="", updated_at="", pagesCount="", finished=""):
        index = self.count()
        widget = ComicItemWidget()
        widget.setFocusPolicy(Qt.NoFocus)
        widget.id = _id
        widget.url = ToolUtil.GetRealUrl(url, path)
        if self.isGame:
            widget.path = ToolUtil.GetRealPath(_id, "game/cover")
        else:
            widget.path = ToolUtil.GetRealPath(_id, "cover")

        widget.index = index
        widget.categoryLabel.setText(categoryStr)
        widget.nameLable.setText(title)
        if updated_at:
            dayStr = ToolUtil.GetUpdateStr(updated_at)
            updateStr = dayStr + Str.GetStr(Str.Update)
            widget.timeLabel.setText(updateStr)
            widget.timeLabel.setVisible(True)
        else:
            widget.timeLabel.setVisible(False)

        if likesCount:
            widget.starButton.setText(str(likesCount))
            widget.starButton.setVisible(True)
        else:
            widget.starButton.setVisible(False)

        if pagesCount:
            title += "<font color=#d5577c>{}</font>".format("("+str(pagesCount)+"P)")
        if finished:
            title += "<font color=#d5577c>{}</font>".format("({})".format(Str.GetStr(Str.ComicFinished)))

        item = QListWidgetItem(self)
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setSizeHint(widget.sizeHint())
        self.setItemWidget(item, widget)
        widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
        widget.PicLoad.connect(self.LoadingPicture)
        # if url and config.IsLoadingPicture:
        #     self.AddDownloadTask(url, path, completeCallBack=self.LoadingPictureComplete, backParam=index)
        #     pass

    def LoadingPicture(self, index):
        item = self.item(index)
        widget = self.itemWidget(item)
        assert isinstance(widget, ComicItemWidget)
        self.AddDownloadTask(widget.url, widget.path, completeCallBack=self.LoadingPictureComplete, backParam=index)

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            if not widget:
                return
            assert isinstance(widget, ComicItemWidget)
            widget.SetPicture(data)
            if Setting.CoverIsOpenWaifu.value:
                item = self.item(index)
                indexModel = self.indexFromItem(item)
                self.Waifu2xPicture(indexModel, True)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            if not widget:
                return
            assert isinstance(widget, ComicItemWidget)
            widget.SetPictureErr()
        return

    def SelectItem(self, item):
        assert isinstance(item, QListWidgetItem)
        widget = self.itemWidget(item)
        assert isinstance(widget, ComicItemWidget)
        if self.isGame:
            QtOwner().OpenGameInfo(widget.id)
        else:
            QtOwner().OpenBookInfo(widget.id)
        return

    def OpenBookInfoHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            QtOwner().OpenBookInfo(widget.id)
            return

    def OpenPicture(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            QtOwner().OpenWaifu2xTool(widget.picData)
            return

    def ReDownloadPicture(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            if widget.url and config.IsLoadingPicture:
                widget.SetPicture("")
                item = self.itemFromIndex(index)
                count = self.row(item)
                widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
                self.AddDownloadTask(widget.url, widget.path, completeCallBack=self.LoadingPictureComplete, backParam=count, isReload=True)
                pass

    def Waifu2xPicture(self, index, isIfSize=False):
        widget = self.indexWidget(index)
        assert isinstance(widget, ComicItemWidget)
        if widget and widget.picData:
            w, h, mat = ToolUtil.GetPictureSize(widget.picData)
            if max(w, h) <= Setting.CoverMaxNum.value or not isIfSize:
                model = ToolUtil.GetModelByIndex(Setting.CoverLookNoise.value, Setting.CoverLookScale.value, Setting.CoverLookModel.value, mat)
                widget.isWaifu2xLoading = True
                self.AddConvertTask(widget.path, widget.picData, model, self.Waifu2xPictureBack, index)

    def CancleWaifu2xPicture(self, index):
        widget = self.indexWidget(index)
        assert isinstance(widget, ComicItemWidget)
        if widget.isWaifu2x and widget.picData:
            widget.SetPicture(widget.picData)

    def Waifu2xPictureBack(self, data, waifuId, index, tick):
        widget = self.indexWidget(index)
        if data and widget:
            assert isinstance(widget, ComicItemWidget)
            widget.SetWaifu2xData(data)
        return

    def CopyHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            data = widget.GetTitle() + str("\r\n")
            clipboard = QApplication.clipboard()
            data = data.strip("\r\n")
            clipboard.setText(data)
        pass

    def DelHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            self.DelCallBack(widget.id)

    def DelCallBack(self, cfgId):
        return

    def DownloadHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            QtOwner().OpenEpsInfo(widget.id)
        pass