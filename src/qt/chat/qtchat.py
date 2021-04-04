import weakref

from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout

from src.qt.chat.qtchatroom import QtChatRoom
from src.qt.com.qtlistwidget import QtBookList
from src.server import Server, QtTask, req, Log, json


class QtChat(QtWidgets.QWidget):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        self.owner = weakref.ref(owner)
        self.gridLayout = QGridLayout(self)
        self.listWidget = QtBookList(None, self.__class__.__name__, owner)
        self.listWidget.InitUser()
        self.gridLayout.addWidget(self.listWidget)
        self.closeFlag = self.__class__.__name__
        self.listWidget.doubleClicked.connect(self.OpenChatRoom)
        self.chatRoom = QtChatRoom()

    def SwitchCurrent(self):
        if self.listWidget.count() > 0:
            return
        QtTask().AddHttpTask(
            lambda x: Server().Send(req.GetChatReq(), bakParam=x),
            self.GetChatBack, cleanFlag=self.closeFlag)
        return

    def GetChatBack(self, data):
        try:
            data = json.loads(data)
            if data.get("code") == 200:
                infos = data.get("data", {}).get("chatList", {})
                for index, info in enumerate(infos):
                    name = info.get("title")
                    content = info.get("description")
                    # avatar = info.get("_user", {}).get("avatar", {})
                    # createdTime = info.get("created_at")
                    self.listWidget.AddUserItem(info.get("url"), "", "", content, name, "", index+1,
                                                info.get("avatar"),
                                                "", "")
        except Exception as es:
            Log.Error(es)
        return

    def OpenChatRoom(self, modelIndex):
        index = modelIndex.row()
        item = self.listWidget.item(index)
        if not item:
            return
        widget = self.listWidget.itemWidget(item)
        if not widget:
            return
        self.chatRoom.OpenChat(widget.id, widget.nameLabel.text())