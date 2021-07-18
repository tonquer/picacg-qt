from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout

from src.qt.chat.qtchatroom import QtChatRoom
from src.qt.qtmain import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req, Log, json, Status
from ui.qtlistwidget import QtBookList


class QtChat(QtWidgets.QWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        QtTaskBase.__init__(self)
        self.gridLayout = QGridLayout(self)
        self.listWidget = QtBookList(None)
        self.listWidget.InitUser()
        self.gridLayout.addWidget(self.listWidget)
        self.listWidget.doubleClicked.connect(self.OpenChatRoom)
        self.chatRoom = QtChatRoom()
        self.listWidget.setStyleSheet("""
        QListWidget {background-color:transparent;}
        """)

    def SwitchCurrent(self):
        if self.listWidget.count() > 0:
            return
        QtOwner().owner.loadingForm.show()
        self.AddHttpTask(req.GetChatReq(), self.GetChatBack)
        return

    def GetChatBack(self, data):
        QtOwner().owner.loadingForm.close()
        try:
            data = json.loads(data)
            if data.get("code") == 200:
                infos = data.get("data", {}).get("chatList", {})
                for index, info in enumerate(infos):
                    self.listWidget.AddUserItem(info, index+1)
        except Exception as es:
            Log.Error(es)
            QtOwner().owner.msgForm.ShowMsg(Status.UnKnowError)
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