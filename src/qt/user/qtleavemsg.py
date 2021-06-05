import weakref

from PySide2 import QtWidgets
from PySide2.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QPushButton

from src.qt.com.qtbubblelabel import QtBubbleLabel
from ui.qtlistwidget import QtBookList
from src.server import Server, req, json, Log, QtTask
from ui.leavemsg import Ui_LeaveMsg


class QtLeaveMsg(QtWidgets.QWidget, Ui_LeaveMsg):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_LeaveMsg.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.closeFlag = self.__class__.__name__
        # self.gridLayout_3.addWidget(self.listWidget, 0, 0, 1, 1)

        self.listWidget.InitUser("leave_msg1", owner, self.LoadNextPage)
        self.listWidget.doubleClicked.connect(self.OpenCommentInfo)

        self.childrenListWidget = QtBookList(None)
        self.childrenListWidget.InitUser("leave_msg2", owner, self.LoadChildrenNextPage)

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

        # self.gridLayout_3.addWidget(self.listWidget)
        # layout = QHBoxLayout()
        # self.commentLine = QLineEdit()
        # layout.addWidget(self.commentLine)
        # self.commentButton = QPushButton("发送评论")
        # layout.addWidget(self.commentButton)
        # self.gridLayout_3.addLayout(layout, 1, 0)
        self.commentButton.clicked.connect(self.SendComment)
        self.bookId = "5822a6e3ad7ede654696e482"

    @property
    def loadingForm(self):
        return self.owner().loadingForm

    def SwitchCurrent(self):
        self.loadingForm.show()
        self.listWidget.UpdatePage(1, 1)
        self.nums.setText("分页：{}/{}".format(str(1), str(1)))
        self.childrenListWidget.UpdatePage(1, 1)
        self.childrenListWidget.UpdateState()
        self.listWidget.UpdateState()
        QtTask().AddHttpTask(
            lambda x: Server().Send(req.GetComments(self.bookId, self.listWidget.page), bakParam=x),
            self.GetCommnetBack, cleanFlag=self.closeFlag)
        return

    def JumpPage(self):
        try:
            page = int(self.spinBox.text())
            if page > self.listWidget.pages:
                return
            self.listWidget.page = page
            self.listWidget.clear()
            self.loadingForm.show()
            QtTask().AddHttpTask(
                lambda x: Server().Send(req.GetComments(self.bookId, self.listWidget.page), bakParam=x),
                self.GetCommnetBack, cleanFlag=self.closeFlag)
        except Exception as es:
            Log.Error(es)

    def OpenCommentInfo(self, modelIndex):
        index = modelIndex.row()
        item = self.listWidget.item(index)
        if not item:
            return
        widget = self.listWidget.itemWidget(item)
        if not widget:
            return

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

        self.loadingForm.show()
        QtTask().AddHttpTask(lambda x: Server().Send(req.GetCommentsChildrenReq(widget.id), bakParam=x),
                                        self.LoadCommentInfoBack, backParam=index, cleanFlag=self.closeFlag)

    def LoadNextPage(self):
        self.loadingForm.show()
        QtTask().AddHttpTask(
            lambda x: Server().Send(req.GetComments(self.bookId, self.listWidget.page + 1), bakParam=x),
            self.GetCommnetBack, cleanFlag=self.closeFlag)
        return

    def LoadChildrenNextPage(self):
        index = self.childrenListWidget.parentId
        item = self.listWidget.item(index)
        if not item:
            return
        widget = self.listWidget.itemWidget(item)
        if not widget:
            return
        self.loadingForm.show()
        QtTask().AddHttpTask(lambda x: Server().Send(req.GetCommentsChildrenReq(widget.id, self.childrenListWidget.page + 1), bakParam=x),
                                        self.LoadCommentInfoBack, backParam=index, cleanFlag=self.closeFlag)
        return

    def LoadCommentInfoBack(self, msg, index):
        try:
            self.loadingForm.close()
            item = self.listWidget.item(index)
            if not item:
                return
            widget = self.listWidget.itemWidget(item)
            if not widget:
                return
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

    # 加载评论
    def GetCommnetBack(self, data):
        try:
            self.loadingForm.close()
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
        self.loadingForm.show()
        QtTask().AddHttpTask(lambda x: Server().Send(req.SendComment(self.bookId, data), bakParam=x), callBack=self.SendCommentBack)

    def SendCommentBack(self, msg):
        try:
            data = json.loads(msg)
            if data.get("code") == 200:
                self.ClearCommnetList()
                QtTask().AddHttpTask(lambda x: Server().Send(req.GetComments(self.bookId), bakParam=x),
                                                self.GetCommnetBack, cleanFlag=self.closeFlag)
            else:
                self.loadingForm.close()
                QtBubbleLabel.ShowErrorEx(self, data.get("message", "错误"))
            self.commentLine.setText("")
        except Exception as es:
            self.loadingForm.close()
            Log.Error(es)

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
        self.loadingForm.show()
        self.childrenListWidget.clear()
        QtTask().AddHttpTask(lambda x: Server().Send(req.SendCommentChildrenReq(commentId, data), bakParam=x), callBack=self.SendCommentChildrenBack, backParam=index)

    def SendCommentChildrenBack(self, msg, index):
        try:
            item = self.listWidget.item(index)
            if not item:
                self.loadingForm.close()
                return
            widget = self.listWidget.itemWidget(item)
            if not widget:
                self.loadingForm.close()
                return

            data = json.loads(msg)
            if data.get("code") == 200:
                QtTask().AddHttpTask(
                    lambda x: Server().Send(req.GetCommentsChildrenReq(widget.id), bakParam=x),
                    self.LoadCommentInfoBack, backParam=index, cleanFlag=self.closeFlag)
            else:
                self.loadingForm.close()
                QtBubbleLabel.ShowErrorEx(self, data.get("message", "错误"))
            self.commentLine.setText("")
        except Exception as es:
            self.loadingForm.close()
            Log.Error(es)

    def ClearCommnetList(self):
        if self.childrenListWidget.parentId >= 0:
            item2 = self.listWidget.item(self.childrenListWidget.parentId)
            widget2 = self.listWidget.itemWidget(item2)
            self.childrenWidget.setParent(None)
            widget2.gridLayout.removeWidget(self.childrenWidget)
            self.childrenListWidget.parentId = -1
            item2.setSizeHint(widget2.sizeHint())
        self.childrenListWidget.clear()
        self.listWidget.clear()
