from component.list.comic_list_widget import ComicListWidget
from component.widget.comic_item_widget import ComicItemWidget


class DownloadAllItem:
    def __init__(self):
        self.bookId = 0
        self.isAllChip = True
        self.isAll = True
        self.tableRow = 0
        self.title = ""
        self.pages = ""
        self.category = ""

    @staticmethod
    def MakeAllItem(self):
        assert isinstance(self, ComicListWidget)
        allData = []
        allCount = self.count()
        for i in range(0, allCount):
            item = self.item(i)
            widget = self.itemWidget(item)
            if isinstance(widget, ComicItemWidget):
                data = DownloadAllItem()
                data.bookId = widget.id
                data.pages = widget.picNum
                data.category = widget.category
                data.title = widget.title
                allData.append(data)
        return allData
