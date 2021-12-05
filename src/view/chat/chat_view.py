import json

from PySide6.QtWidgets import QWidget

from interface.ui_chat import Ui_Chat
from qt_owner import QtOwner
from server import req, Log, Status
from task.qt_task import QtTaskBase
from tools.str import Str
from view.chat.chat_room_widget import ChatRoomWidget


class ChatView(QWidget, Ui_Chat, QtTaskBase):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Chat.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.listWidget.itemClicked.connect(self.OpenChatRoom)
        self.chatRoom = ChatRoomWidget()

    def Stop(self):
        self.chatRoom.Stop()

    def SwitchCurrent(self, **kwargs):
        if self.listWidget.count() > 0:
            return
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetChatReq(), self.GetChatBack)
        return

    def GetChatBack(self, raw):
        QtOwner().CloseLoading()
        try:
            st = raw["st"]
            data = json.loads(raw["data"])
            if data.get("code") == 200:
                infos = data.get("data", {}).get("chatList", {})
                for index, info in enumerate(infos):
                    self.listWidget.AddUserItem(info, index+1, True)
        except Exception as es:
            Log.Error(es)
            QtOwner().ShowMsg(Str.GetStr(Status.UnKnowError))
        return

    def OpenChatRoom(self, item):
        widget = self.listWidget.itemWidget(item)
        if not widget:
            return
        self.chatRoom.OpenChat(widget.id, widget.titleLabel.text())
