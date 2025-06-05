from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsProxyWidget, QGraphicsPixmapItem, QLabel

from tools.singleton import Singleton
from view.read.read_qgraphics_proxy_widget import ReadQGraphicsProxyWidget


class QtReadImgPoolManager(Singleton):
    def __init__(self):
        self.proxyNum = 300    # QGraphicsProxyWidget
        self.pixMapNum = 3     # QGraphicsPixmapItem

        self.proxyItem = []
        self.pixMapItem = []

    def GetProxyItem(self):
        if not self.proxyItem:
            a = QGraphicsProxyWidget()
            a.setWidget(QLabel())
            return a
        return self.proxyItem.pop()

    def AddProxyItem(self, item):
        assert isinstance(item, QGraphicsProxyWidget)
        # if item.widget():
        #     item.widget().setParent(None)
            # item.setWidget(None)
        item.setPos(0, 0)
        self.proxyItem.append(item)

    def GetPixMapItem(self):
        if not self.pixMapItem:
            return QGraphicsPixmapItem()
        return self.pixMapItem.pop()

    def AddPixMapItem(self, item):
        assert isinstance(item, QGraphicsPixmapItem)
        item.setPixmap(QPixmap())

        # item.widget().clear()
        item.setPos(0, 0)
        self.pixMapItem.append(item)
