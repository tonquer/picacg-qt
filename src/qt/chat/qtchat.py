import weakref

from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout

from src.qt.chat.qtchatroom import QtChatRoom
from ui.qtlistwidget import QtBookList
from src.server import Server, QtTask, req, Log, json, Status


class QtChat(QtWidgets.QWidget):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        self.owner = weakref.ref(owner)
        self.gridLayout = QGridLayout(self)
        self.listWidget = QtBookList(None)
        self.listWidget.InitUser(self.__class__.__name__, owner)
        self.gridLayout.addWidget(self.listWidget)
        self.closeFlag = self.__class__.__name__
        self.listWidget.doubleClicked.connect(self.OpenChatRoom)
        self.chatRoom = QtChatRoom()
        self.listWidget.setStyleSheet("""
        QListWidget {background-color:transparent;}
        """)

    def SwitchCurrent(self):
        if self.listWidget.count() > 0:
            return
        self.owner().loadingForm.show()
        QtTask().AddHttpTask(
            lambda x: Server().Send(req.GetChatReq(), bakParam=x),
            self.GetChatBack, cleanFlag=self.closeFlag)
        return

    def GetChatBack(self, data):
        self.owner().loadingForm.close()
        try:
            data = json.loads(data)
            if data.get("code") == 200:
                infos = data.get("data", {}).get("chatList", {})
                for index, info in enumerate(infos):
                    name = info.get("title")
                    content = info.get("description")
                    # avatar = info.get("_user", {}).get("avatar", {})
                    # createdTime = info.get("created_at")
                    self.listWidget.AddUserItem(info, index+1)
        except Exception as es:
            Log.Error(es)
            self.owner().msgForm.ShowMsg(Status.UnKnowError)
        return

    def OpenChatRoom(self, modelIndex):
        index = modelIndex.row()
        item = self.listWidget.item(index)
        if not item:
            return
        widget = self.listWidget.itemWidget(item)
        if not widget:
            return
        self.chatRoom.OpenChat(widget.id, widget.titleLabel.text())