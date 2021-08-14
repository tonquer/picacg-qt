import json
import weakref

from PySide2 import QtWidgets
from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QPushButton

from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.com.qtloading import QtLoading
from src.qt.util.qttask import QtTaskBase
from src.server import req, Log
from ui.leavemsg import Ui_LeaveMsg
from ui.qtlistwidget import QtBookList


class QtCommentList(QtWidgets.QWidget, Ui_LeaveMsg, QtTaskBase):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Ui_LeaveMsg.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.reqSendComment = None
        self.reqGetComment = None
        self.reqLikeComment = None
        self.loadingForm2 = QtLoading(self)
        self.bookId = ""
        self.listWidget.InitUser(self.LoadNextPage, self.OpenCommentInfo, self.AddLike)

        self.childrenListWidget = QtBookList(None)
        self.childrenListWidget.InitUser(self.LoadChildrenNextPage, likeBack=self.AddLike)
        self.childrenWidget = QtWidgets.QWidget()
        layout = QHBoxLayout(self.childrenWidget)

        label = QLabel()
        label.setMinimumWidth(100)
        layout.addWidget(label)
        layout3 = QVBoxLayout()

        layout2 = QHBoxLayout()
        self.commentLine2 = QLineEdit()
        self.commentButton2 = QPushButton("回复")
        self.commentButton2.clicked.connect(self.SendCommentChildren)
        layout2.addWidget(self.commentLine2)
        layout2.addWidget(self.commentButton2)
        layout3.addLayout(layout2)
        layout3.addWidget(self.childrenListWidget)
        layout.addLayout(layout3)

    def InitReq(self, reqGetComment, reqSendComment, reqLikeComment):
        self.reqSendComment = reqSendComment
        self.reqGetComment = reqGetComment
        self.reqLikeComment = reqLikeComment

    def SendCommentChildren(self):
        data = self.commentLine2.text()
        if not data:
            return
        index = self.childrenListWidget.parentId
        item = self.listWidget.item(index)
        if not item:
            return
        widget = self.listWidget.itemWidget(item)
        if not widget:
            return
        self.commentLine2.setText("")
        commentId = widget.id
        self.loadingForm2.show()
        self.childrenListWidget.clear()
        self.AddHttpTask(req.SendCommentChildrenReq(commentId, data), callBack=self.SendCommentChildrenBack, backParam=index)

    def SendCommentChildrenBack(self, msg, index):
        try:
            item = self.listWidget.item(index)
            if not item:
                self.loadingForm2.close()
                return
            widget = self.listWidget.itemWidget(item)
            if not widget:
                self.loadingForm2.close()
                return

            data = json.loads(msg)
            if data.get("code") == 200:
                self.AddHttpTask(req.GetCommentsChildrenReq(widget.id), self.LoadCommentInfoBack, backParam=index)
            else:
                self.loadingForm2.close()
                QtBubbleLabel.ShowErrorEx(self, data.get("message", "错误"))
            self.commentLine2.setText("")
        except Exception as es:
            self.loadingForm2.close()
            Log.Error(es)

    def OpenCommentInfo(self, cfgId):
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            if not item:
                continue
            widget = self.listWidget.itemWidget(item)
            if not widget:
                continue
            if widget.id != cfgId:
                continue

            self.listWidget.SetWheelStatus(True)
            self.childrenListWidget.clear()
            self.childrenListWidget.UpdatePage(1, 1)
            self.childrenListWidget.UpdateState()
            if self.childrenListWidget.parentId == index:
                # self.childrenWidget.hide()
                self.childrenWidget.setParent(None)
                widget.gridLayout.removeWidget(self.childrenWidget)
                self.childrenListWidget.parentId = -1
                item.setSizeHint(widget.sizeHint())
                return
            if self.childrenListWidget.parentId >= 0:
                item2 = self.listWidget.item(self.childrenListWidget.parentId)
                widget2 = self.listWidget.itemWidget(item2)
                self.childrenWidget.setParent(None)
                widget2.gridLayout.removeWidget(self.childrenWidget)
                self.childrenListWidget.parentId = -1
                item2.setSizeHint(widget2.sizeHint())

            self.loadingForm2.show()
            self.AddHttpTask(req.GetCommentsChildrenReq(widget.id), self.LoadCommentInfoBack, backParam=index)

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

            self.loadingForm2.show()
            self.AddHttpTask(self.reqLikeComment(widget.id), self.CommentsLikeBack, backParam=cfgId)

        for index in range(self.childrenListWidget.count()):
            item = self.childrenListWidget.item(index)
            if not item:
                continue
            widget = self.childrenListWidget.itemWidget(item)
            if not widget:
                continue
            if widget.id != cfgId:
                continue

            self.loadingForm2.show()
            self.AddHttpTask(self.reqLikeComment(widget.id), self.CommentsLikeBack, backParam=cfgId)

    def CommentsLikeBack(self, data, cfgId):
        self.loadingForm2.close()
        data = json.loads(data)
        if data.get("code") != 200:
            return
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

        for index in range(self.childrenListWidget.count()):
            item = self.childrenListWidget.item(index)
            if not item:
                continue
            widget = self.childrenListWidget.itemWidget(item)
            if not widget:
                continue
            if widget.id != cfgId:
                continue
            widget.SetLike(isLike)
            widget.update()
        self.update()

    def LoadChildrenNextPage(self):
        index = self.childrenListWidget.parentId
        item = self.listWidget.item(index)
        if not item:
            return
        widget = self.listWidget.itemWidget(item)
        if not widget:
            return
        self.loadingForm2.show()
        self.AddHttpTask(req.GetCommentsChildrenReq(widget.id, self.childrenListWidget.page + 1), self.LoadCommentInfoBack, backParam=index)
        return

    def LoadCommentInfoBack(self, msg, index):
        try:
            self.loadingForm2.close()
            item = self.listWidget.item(index)
            if not item:
                return
            widget = self.listWidget.itemWidget(item)
            if not widget:
                return
            self.listWidget.ClearWheelEvent()
            self.listWidget.SetWheelStatus(False)

            self.childrenListWidget.UpdateState()
            data = json.loads(msg)
            self.childrenListWidget.parentId = index
            widget.gridLayout.addWidget(self.childrenWidget, 1, 0, 1, 1)
            if data.get("code") == 200:
                comments = data.get("data", {}).get("comments", {})
                page = int(comments.get("page", 1))
                total = int(comments.get("total", 1))
                pages = int(comments.get("pages", 1))
                limit = int(comments.get("limit", 1))
                self.childrenListWidget.UpdatePage(page, pages)
                for index, info in enumerate(comments.get("docs")):
                    floor = total - ((page - 1) * limit + index)
                    self.childrenListWidget.AddUserItem(info, floor)

                pass
            self.listWidget.scrollToItem(item, self.listWidget.ScrollHint.PositionAtTop)
            size = self.listWidget.size()
            item.setSizeHint(size)
        except Exception as es:
            Log.Error(es)

    def ClearCommnetList(self):
        self.listWidget.SetWheelStatus(True)
        if self.childrenListWidget.parentId >= 0:
            item2 = self.listWidget.item(self.childrenListWidget.parentId)
            widget2 = self.listWidget.itemWidget(item2)
            self.childrenWidget.setParent(None)
            widget2.gridLayout.removeWidget(self.childrenWidget)
            self.childrenListWidget.parentId = -1
            item2.setSizeHint(widget2.sizeHint())
        self.childrenListWidget.clear()
        self.listWidget.clear()
        self.childrenListWidget.UpdatePage(1, 1)
        self.childrenListWidget.UpdateState()
        self.listWidget.UpdatePage(1, 1)
        self.listWidget.UpdateState()
        self.spinBox.setValue(1)
        self.nums.setText("分页：{}/{}".format(str(1), str(1)))
        self.ClearTask()

    def JumpPage(self):
        try:
            page = int(self.spinBox.text())
            if page > self.listWidget.pages:
                return
            self.listWidget.SetWheelStatus(True)
            self.listWidget.page = page
            self.listWidget.clear()
            self.loadingForm2.show()
            self.AddHttpTask(self.reqGetComment(self.bookId, self.listWidget.page), self.GetCommnetBack)
        except Exception as es:
            Log.Error(es)

    def LoadComment(self):
        self.ClearCommnetList()
        self.AddHttpTask(self.reqGetComment(self.bookId, self.listWidget.page), self.GetCommnetBack)
        return

    def LoadNextPage(self):
        self.loadingForm2.show()
        self.AddHttpTask(self.reqGetComment(self.bookId, self.listWidget.page + 1), self.GetCommnetBack)
        return

    # 加载评论
    def GetCommnetBack(self, data):
        try:
            self.loadingForm2.close()
            self.listWidget.UpdateState()
            msg = json.loads(data)
            if msg.get("code") == 200:
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
                        floor = "置顶"
                        self.listWidget.AddUserItem(info, floor)

                for index, info in enumerate(comments.get("docs")):
                    floor = total - ((page - 1) * limit + index)
                    self.listWidget.AddUserItem(info, floor)
            return
        except Exception as es:
            Log.Error(es)

    def SendComment(self):
        data = self.commentLine.text()
        if not data:
            return
        self.commentLine.setText("")
        self.loadingForm2.show()
        self.AddHttpTask(self.reqSendComment(self.bookId, data), callBack=self.SendCommentBack)

    def SendCommentBack(self, msg):
        try:
            data = json.loads(msg)
            if data.get("code") == 200:
                self.ClearCommnetList()
                self.AddHttpTask(self.reqGetComment(self.bookId), self.GetCommnetBack)
            else:
                self.loadingForm2.close()
                QtBubbleLabel.ShowErrorEx(self, data.get("message", "错误"))
            self.commentLine.setText("")
        except Exception as es:
            self.loadingForm2.close()
            Log.Error(es)
