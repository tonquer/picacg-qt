import json

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from interface.ui_comment import Ui_Comment
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.str import Str
from tools.user import User


class CommentWidget(QtWidgets.QWidget, Ui_Comment, QtTaskBase):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Comment.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)
        self.reqSendComment = None
        self.reqGetComment = None
        self.reqLikeComment = None
        self.reqKillComment = None
        self.listWidget.LoadCallBack = self.LoadNextPage

        self.bookId = ""
        self.default = "5822a6e3ad7ede654696e482"
        self.eventId = ""
        self.pushButton.clicked.connect(self.SendComment)
        self.skipButton.clicked.connect(self.JumpPage)

    def SwitchCurrent(self, **kwargs):
        bookId = kwargs.get("bookId")
        refresh = kwargs.get("refresh")
        if not bookId and self.listWidget.count() > 0 and not refresh:
            return

        self.bookId = bookId
        if not self.bookId:
            self.bookId = self.default

        self.LoadComment()
        pass

    def InitReq(self, reqGetComment, reqSendComment, reqLikeComment, reqKillComment):
        self.reqSendComment = reqSendComment
        self.reqGetComment = reqGetComment
        self.reqLikeComment = reqLikeComment
        self.reqKillComment = reqKillComment

    def AddLike(self, cfgId):
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            if not item:
                continue
            widget = self.listWidget.itemWidget(item)
            if not widget:
                continue
            if widget.id != cfgId:
                continue

            QtOwner().ShowLoading()
            self.AddHttpTask(self.reqLikeComment(widget.id), self.CommentsLikeBack, backParam=cfgId)

    def CommentsLikeBack(self, raw, cfgId):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st != Status.Ok:
            QtOwner().ShowMsg(Str.GetStr(st))
            return
        data = json.loads(raw["data"])
        isLike = False
        if data.get("data").get("action") == "like":
            isLike = True
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            if not item:
                continue
            widget = self.listWidget.itemWidget(item)
            if not widget:
                continue
            if widget.id != cfgId:
                continue
            widget.SetLike(isLike)

    def KillComment(self, cfgId):
        return
        # for index in range(self.listWidget.count()):
        #     item = self.listWidget.item(index)
        #     if not item:
        #         continue
        #     widget = self.listWidget.itemWidget(item)
        #     if not widget:
        #         continue
        #     if widget.id != cfgId:
        #         continue
        #     r = QtOwner().ShowMsgBox(QMessageBox.Question, self.tr('举报'),
        #                              self.tr('是否举报') + widget.nameLabel.text() + ",\n" + self.tr(
        #                                  "评论：") +"\n"+ widget.commentLabel.text() + "\n")
        #     if r == 0:
        #         QtOwner().ShowLoading()
        #         self.AddHttpTask(self.reqKillComment(widget.id), self.KillCommentBack, backParam=cfgId)

    def KillCommentBack(self, raw, backId):
        QtOwner().CloseLoading()
        try:
            st = raw["st"]
            if st != Status.Ok:
                QtOwner().ShowMsg(Str.GetStr(st))
                return
            data = json.loads(raw["data"])
            if data.get("code") != 200:
                return
            QtOwner().ShowMsg(data.get('data').get("message", ""))
        except Exception as es:
            Log.Error(es)

    def ClearCommnetList(self):
        self.listWidget.SetWheelStatus(True)
        self.listWidget.clear()
        self.listWidget.UpdatePage(1, 1)
        self.listWidget.UpdateState()
        # self.spinBox.setValue(1)
        # self.nums.setText("分页：{}/{}".format(str(1), str(1)))
        self.ClearTask()

    def JumpPage(self):
        try:
            page = int(self.spinBox.text())
            if page > self.listWidget.pages:
                return
            self.listWidget.SetWheelStatus(True)
            self.listWidget.page = page
            self.listWidget.clear()
            QtOwner().ShowLoading()
            self.AddHttpTask(self.reqGetComment(self.bookId, self.listWidget.page), self.GetCommnetBack)
        except Exception as es:
            Log.Error(es)

    def LoadComment(self):
        QtOwner().ShowLoading()
        self.ClearCommnetList()
        self.AddHttpTask(self.reqGetComment(self.bookId, self.listWidget.page), self.GetCommnetBack)
        return

    def LoadNextPage(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(self.reqGetComment(self.bookId, self.listWidget.page + 1), self.GetCommnetBack)
        return

    # 加载评论
    def GetCommnetBack(self, raw):
        try:
            QtOwner().CloseLoading()
            self.listWidget.UpdateState()
            st = raw["st"]
            if st == Status.Ok:

                msg = json.loads(raw["data"])
                comments = msg.get("data", {}).get("comments", {})
                topComments = msg.get("data", {}).get("topComments", [])
                page = int(comments.get("page", 1))
                pages = int(comments.get("pages", 1))
                limit = int(comments.get("limit", 1))
                self.listWidget.UpdatePage(page, pages)
                self.spinBox.setValue(page)
                self.spinBox.setMaximum(pages)
                self.nums.setText("分页：{}/{}".format(str(page), str(pages)))
                total = comments.get("total", 0)
                # self.tabWidget.setTabText(1, "评论({})".format(str(total)))
                if page == 1:
                    for index, info in enumerate(topComments):
                        floor = Str.GetStr(Str.Top)
                        self.listWidget.AddUserItem(info, floor, likeCallBack=self.AddLike)

                for index, info in enumerate(comments.get("docs")):
                    if self.reqGetComment == req.GetUserCommentReq:
                        info["_user"] = User().userInfo
                    floor = total - ((page - 1) * limit + index)
                    self.listWidget.AddUserItem(info, floor, likeCallBack=self.AddLike)
            else:
                QtOwner().ShowError(Str.GetStr(st))
            return
        except Exception as es:
            QtOwner().ShowError(Str.GetStr(Str.CommentLoadFail))
            Log.Error(es)

    def SendComment(self):
        data = self.commentLine.text()
        if not data:
            return
        self.commentLine.setText("")
        QtOwner().ShowLoading()
        self.AddHttpTask(self.reqSendComment(self.bookId, data), callBack=self.SendCommentBack)

    def SendCommentBack(self, raw):
        try:
            data = json.loads(raw["data"])
            st = raw["st"]
            if st == Status.Ok:
                if data.get("code") == 200:
                    self.ClearCommnetList()
                    self.commentLine.setText("")
                    self.AddHttpTask(self.reqGetComment(self.bookId), self.GetCommnetBack)
                else:
                    QtOwner().CloseLoading()
                    QtOwner().ShowError(data.get("message", Str.GetStr(Str.Error)))
            else:
                QtOwner().ShowError(Str.GetStr(st))

        except Exception as es:
            QtOwner().CloseLoading()
            Log.Error(es)
