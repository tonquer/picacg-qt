from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsProxyWidget, QGraphicsPixmapItem, QLabel

from tools.singleton import Singleton
from view.read.read_new_graphics_item import ReadNewGraphicsItem


class ReadNewPoolManager(Singleton):
    def __init__(self):
        self.proxyNum = 300    # QGraphicsProxyWidget
        self.pixMapNum = 3     # QGraphicsPixmapItem

        self.proxyItem = []

    def GetProxyItem(self):
        # return ReadNewGraphicsItem(-1)
        if not self.proxyItem:
            a = ReadNewGraphicsItem(-1)
            return a
        return self.proxyItem.pop()

    def AddProxyItem(self, item: ReadNewGraphicsItem):
        # del item
        item.init()
        item.setPos(0, 0)
        self.proxyItem.append(item)
