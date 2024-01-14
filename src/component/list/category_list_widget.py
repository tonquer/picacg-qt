from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QCursor
from PySide6.QtWidgets import QListWidgetItem, QMenu, QListView

from component.list.base_list_widget import BaseListWidget
from component.widget.comic_item_widget import ComicItemWidget
from config import config
from config.setting import Setting
from qt_owner import QtOwner
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class CategoryListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.resize(800, 600)
        # self.setMinimumHeight(400)
        self.setFrameShape(QListView.NoFrame)  # 无边框
        self.setFlow(QListView.LeftToRight)  # 从左到右
        self.setWrapping(True)
        self.setResizeMode(QListView.Adjust)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.SelectMenuBook)
        # self.doubleClicked.connect(self.OpenBookInfo)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def SelectMenuBook(self, pos):
        index = self.indexAt(pos)
        widget = self.indexWidget(index)
        if index.isValid() and widget:
            popMenu = QMenu(self)
            action = popMenu.addAction(Str.GetStr(Str.LookCover))
            action.triggered.connect(partial(self.OpenPicture, index))
            action = popMenu.addAction(Str.GetStr(Str.ReDownloadCover))
            action.triggered.connect(partial(self.ReDownloadPicture, index))
            assert isinstance(widget, ComicItemWidget)
            if config.CanWaifu2x and widget.picData:
                if not widget.isWaifu2x:
                    action = popMenu.addAction(Str.GetStr(Str.Waifu2xConvert))
                    action.triggered.connect(partial(self.Waifu2xPicture, index))
                    if widget.isWaifu2xLoading or not config.CanWaifu2x:
                        action.setEnabled(False)
                else:
                    action = popMenu.addAction(Str.GetStr(Str.DelWaifu2xConvert))
                    action.triggered.connect(partial(self.CancleWaifu2xPicture, index))
            popMenu.exec_(QCursor.pos())
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

    def AddBookItem(self, _id, title, url="", path=""):
        index = self.count()
        widget = ComicItemWidget(isCategory=True)
        widget.setFocusPolicy(Qt.NoFocus)
        widget.id = _id
        widget.url = ToolUtil.GetRealUrl(url, path)
        widget.path = ToolUtil.GetRealPath(path, "category")
        widget.index = index
        # widget.categoryLabel.setText(categories)
        widget.categoryLabel.hide()
        widget.starButton.hide()
        widget.timeLabel.hide()
        widget.nameLable.setText(title)
        widget.nameLable.setAlignment(Qt.AlignHCenter)

        item = QListWidgetItem(self)
        item.setSizeHint(widget.sizeHint())
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
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
            assert isinstance(widget, ComicItemWidget)
            widget.SetPicture(data)
            if Setting.CoverIsOpenWaifu.value:
                item = self.item(index)
                indexModel = self.indexFromItem(item)
                self.Waifu2xPicture(indexModel, True)
            pass
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            assert isinstance(widget, ComicItemWidget)
            widget.SetPictureErr(status)
        return

    def Waifu2xPicture(self, index, isIfSize=False):
        widget = self.indexWidget(index)
        if widget and widget.picData:
            assert isinstance(widget, ComicItemWidget)
            w, h, mat,_ = ToolUtil.GetPictureSize(widget.picData)
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

    def GetAllSelectItem(self):
        data = set()
        for i in range(self.count()):
            item = self.item(i)
            if item.background().color() == QColor(87, 195, 194):
                data.add(item.text())
        return data
