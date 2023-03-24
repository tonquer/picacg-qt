import base64
import json

from PySide6.QtWidgets import QWidget

from config.setting import Setting
from interface.ui_chat import Ui_Chat
from qt_owner import QtOwner
from server import req, Log, Status
from task.qt_task import QtTaskBase
from tools.str import Str
from view.chat_new.chat_new_room_widget import ChatNewRoomWidget


class ChatNewView(QWidget, Ui_Chat, QtTaskBase):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Chat.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.listWidget.itemClicked.connect(self.OpenChatRoom)
        self.chatRoom = ChatNewRoomWidget()
        self.token = ""
        self.roleProfile = None

    def Stop(self):
        self.chatRoom.Stop()

    def SwitchCurrent(self, **kwargs):
        if self.listWidget.count() > 0:
            return
        QtOwner().ShowLoading()
        userId = Setting.UserId.value
        if not (userId and isinstance(userId, str)):
            userId = ""

        passwd = Setting.Password.value
        passwd = base64.b64decode(passwd).decode("utf-8") if passwd else ""
        if not (passwd and isinstance(passwd, str)):
            passwd = ""
        QtOwner().ShowLoading()
        if not self.token:
            self.AddHttpTask(req.GetNewChatLoginReq(userId, passwd), self.LoginBack)
            return
        if not self.roleProfile:
            self.AddHttpTask(req.GetNewChatProfileReq(self.token), self.GetNewChatProfileBack)
            return

        self.AddHttpTask(req.GetChatReq(), self.GetChatBack)
        return

    def LoginBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            try:
                data = json.loads(raw["data"])
                token = data.get("token")
                if not token:
                    QtOwner().ShowMsg(Str.GetStr(Str.LoginFail))
                    return
                self.token = token
                QtOwner().ShowLoading()
                self.AddHttpTask(req.GetNewChatProfileReq(self.token), self.GetNewChatProfileBack)
            except Exception as es:
                Log.Warn(raw)
                Log.Error(es)
                QtOwner().ShowMsg(Str.GetStr(Status.UnKnowError))
        else:
            QtOwner().ShowError(Str.GetStr(st))
        return

    def GetNewChatProfileBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            try:
                data = json.loads(raw["data"])
                profile = data.get("profile")
                if not profile:
                    QtOwner().ShowMsg(Str.GetStr(Str.LoginFail))
                    return
                self.roleProfile = profile
                QtOwner().ShowLoading()
                self.AddHttpTask(req.GetNewChatReq(self.token), self.GetChatBack)
            except Exception as es:
                Log.Warn(raw)
                Log.Error(es)
                QtOwner().ShowMsg(Str.GetStr(Status.UnKnowError))
        else:
            QtOwner().ShowError(Str.GetStr(st))
        return

    def GetChatBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            try:
                data = json.loads(raw["data"])
                rooms = data.get("rooms")
                for index, info in enumerate(rooms):
                    self.listWidget.AddNewChatItem(info, index+1)
            except Exception as es:
                Log.Warn(raw)
                Log.Error(es)
                QtOwner().ShowMsg(Str.GetStr(Status.UnKnowError))
        else:
            QtOwner().ShowError(Str.GetStr(st))
        return

    def OpenChatRoom(self, item):
        widget = self.listWidget.itemWidget(item)
        if not widget:
            return
        self.chatRoom.OpenChat(self.token, self.roleProfile, widget.id, widget.titleLabel.text())
