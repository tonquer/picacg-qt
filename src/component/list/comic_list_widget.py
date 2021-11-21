from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QListWidgetItem, QMenu, QApplication

from component.list.base_list_widget import BaseListWidget
from component.widget.comic_item_widget import ComicItemWidget
from config import config
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
        if index.isValid():
            popMenu = QMenu(self)
            action = popMenu.addAction(self.tr("打开"))
            action.triggered.connect(partial(self.OpenBookInfoHandler, index))
            action = popMenu.addAction(self.tr("查看封面"))
            action.triggered.connect(partial(self.OpenPicture, index))
            action = popMenu.addAction(self.tr("重下封面"))
            action.triggered.connect(partial(self.ReDownloadPicture, index))
            action = popMenu.addAction(self.tr("复制标题"))
            action.triggered.connect(partial(self.CopyHandler, index))
            action = popMenu.addAction(self.tr("下载"))
            action.triggered.connect(partial(self.DownloadHandler, index))
            if self.isDelMenu:
                action = popMenu.addAction(self.tr("删除"))
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
                categories = self.tr("上次观看到第") + str(info.epsId + 1) + self.tr("章") + "/" + str(v.epsCount) + self.tr(
                    "章")
        self.AddBookItem(_id, title, categories, url, path, likesCount, updated_at, pagesCount, finished)

    def AddBookItemByHistory(self, v):
        _id = v.bookId
        title = v.name
        path = v.path
        url = v.url
        categories = "{}看过".format(ToolUtil.GetUpdateStrByTick(v.tick))
        self.AddBookItem(_id, title, categories, url, path)

    def AddBookItem(self, _id, title, categoryStr="", url="", path="", likesCount="", updated_at="", pagesCount="", finished=""):
        index = self.count()
        widget = ComicItemWidget()
        widget.id = _id
        widget.url = url
        widget.path = path
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
            title += "<font color=#d5577c>{}</font>".format("(完)")

        item = QListWidgetItem(self)
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setSizeHint(widget.sizeHint())
        self.setItemWidget(item, widget)
        widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
        if url and config.IsLoadingPicture:
            self.AddDownloadTask(url, path, None, self.LoadingPictureComplete, True, index, True)
            pass

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            if not widget:
                return
            widget.SetPicture(data)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            if not widget:
                return
            widget.SetPictureErr()
        return

    def SelectItem(self, item):
        assert isinstance(item, QListWidgetItem)
        widget = self.itemWidget(item)
        if self.isGame:
            QtOwner().OpenGameInfo(widget.id)
        else:
            QtOwner().OpenBookInfo(widget.id)
        return

    def OpenBookInfoHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            QtOwner().OpenBookInfo(widget.id)
            return

    def OpenPicture(self, index):
        widget = self.indexWidget(index)
        if widget:
            QtOwner().OpenWaifu2xTool(widget.picData)
            return

    def ReDownloadPicture(self, index):
        widget = self.indexWidget(index)
        if widget:
            if widget.url and config.IsLoadingPicture:
                widget.SetPicture("")
                item = self.itemFromIndex(index)
                count = self.row(item)
                widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
                self.AddDownloadTask(widget.url, widget.path, None, self.LoadingPictureComplete, True, count, False)
                pass

    def CopyHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
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