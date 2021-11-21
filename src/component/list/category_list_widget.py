from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QListWidgetItem

from component.list.base_list_widget import BaseListWidget
from component.widget.comic_item_widget import ComicItemWidget
from config import config
from tools.status import Status
from tools.str import Str


class CategoryListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.resize(800, 600)
        # self.setMinimumHeight(400)
        self.setFrameShape(self.NoFrame)  # 无边框
        self.setFlow(self.LeftToRight)  # 从左到右
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.SelectMenuBook)
        # self.doubleClicked.connect(self.OpenBookInfo)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def AddBookItem(self, _id, title, url="", path=""):
        index = self.count()
        widget = ComicItemWidget()
        widget.url = url
        widget.path = path
        # widget.categoryLabel.setText(categories)
        widget.categoryLabel.hide()
        widget.starButton.hide()
        widget.timeLabel.hide()
        widget.nameLable.setText(title)
        widget.picLabel.setFixedSize(300, 300)
        widget.nameLable.setFixedSize(100, 25)
        widget.nameLable.setAlignment(Qt.AlignHCenter)
        widget.setFixedSize(400, 400)

        item = QListWidgetItem(self)
        item.setSizeHint(widget.sizeHint())
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.setItemWidget(item, widget)
        widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
        if url and config.IsLoadingPicture:
            self.AddDownloadTask(url, path, None, self.LoadingPictureComplete, True, index, True)
            pass

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetPicture(data)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetPictureErr()
        return

    def GetAllSelectItem(self):
        data = set()
        for i in range(self.count()):
            item = self.item(i)
            if item.background().color() == QColor(87, 195, 194):
                data.add(item.text())
        return data
