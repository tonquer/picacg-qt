from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QListView

from component.list.base_list_widget import BaseListWidget
from component.widget.comment_item_widget import CommentItemWidget
from config import config
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class UserListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.NoFrame = QListView.NoFrame
        self.TopToBottom = QListView.TopToBottom
        self.resize(800, 600)
        # self.setMinimumHeight(400)
        # self.setFrameShape(self.NoFrame)  # 无边框
        self.setFlow(self.TopToBottom)
        # self.setWrapping(True)
        # self.setResizeMode(self.Adjust)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.SelectMenuBook)
        # self.doubleClicked.connect(self.OpenBookInfo)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwa ysOff)
        self.setFrameShape(self.NoFrame)  # 无边框
        self.setFocusPolicy(Qt.NoFocus)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("QListWidget::item { border-bottom: 1px solid black; }")

    def AddUserItem(self, info, floor, hideKillButton=False, likeCallBack=None):
        content = info.get("content")
        if not content:
            content = info.get("description")
        if info.get("title"):
            name = info.get("title")
            avatar = info.get("avatar")
            slogan = ""
            level = ""
            title = ""
            character = ""
            uid = ""
        else:
            user = info.get("_user", {})
            uid = user.get("_id")
            name = user.get("name", "")
            avatar = user.get("avatar", {})
            title = user.get("title", "")
            level = user.get("level", 1)
            character = user.get("character", "")
            slogan = user.get("slogan", "")

        createdTime = info.get("created_at", "")
        commentsCount = info.get("commentsCount", "")
        if info.get('_id', ""):
            commnetId = info.get('_id', "")
        else:
            commnetId = info.get("url")
        likesCount = info.get("likesCount", "")

        if not avatar:
            url = ""
            path = ""
        elif isinstance(avatar, str):
            url = avatar
            path = ""
        else:
            url = avatar.get("fileServer", "")
            path = avatar.get("path", "")

        index = self.count()
        iwidget = CommentItemWidget(self)
        iwidget.index = index
        iwidget.setFocusPolicy(Qt.NoFocus)
        if isinstance(info.get("_comic"), dict):
            iwidget.linkId = info.get("_comic").get("_id")
            linkData = info.get("_comic").get("title", "")
            iwidget.linkLabel.setText("<u><font color=#d5577c>{}</font></u>".format(linkData))
            iwidget.linkLabel.setVisible(True)
            iwidget.killButton.setVisible(False)

        if isinstance(info.get("_game"), dict):
            iwidget.linkId = info.get("_game").get("_id")
            linkData = info.get("_game").get("title", "")
            iwidget.isGame = True
            iwidget.linkLabel.setText("GAME: <u><font color=#d5577c>{}</font></u>".format(linkData))
            iwidget.linkLabel.setVisible(True)
            iwidget.killButton.setVisible(False)

        if info.get("isLiked"):
            iwidget.SetLike()

        if likeCallBack:
            iwidget.starButton.clicked.connect(partial(likeCallBack, commnetId))

        if commentsCount == "":
            iwidget.commentButton.hide()

        if likesCount == "":
            iwidget.starButton.hide()
            iwidget.commentLabel.setTextInteractionFlags(Qt.TextSelectableByKeyboard)
        if hideKillButton:
            iwidget.commentLabel.setTextInteractionFlags(Qt.NoTextInteraction)
        iwidget.setToolTip(slogan)
        iwidget.id = commnetId
        iwidget.commentLabel.setText(content)
        iwidget.nameLabel.setText(name)
        iwidget.commentButton.setText("({})".format(commentsCount))
        iwidget.starButton.setText("({})".format(likesCount))
        iwidget.levelLabel.setText(" LV" + str(level) + " ")
        iwidget.titleLabel.setText(" " + title + " ")
        iwidget.url = ToolUtil.GetRealUrl(url, path)
        iwidget.path = ToolUtil.GetRealPath(uid, "user")

        iwidget.character = character
        dayStr = ToolUtil.GetUpdateStr(createdTime)
        iwidget.dateLabel.setText(dayStr)
        iwidget.indexLabel.setText("{}".format(str(floor))+Str.GetStr(Str.Floor))
        iwidget.adjustSize()
        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.setItemWidget(item, iwidget)
        iwidget.PicLoad.connect(self.LoadingPicture)
        # if url and config.IsLoadingPicture:
        #     self.AddDownloadTask(url, path, completeCallBack=self.LoadingPictureComplete, backParam=index)
        # if "pica-web.wakamoment.tk" not in character and character and config.IsLoadingPicture:
        #     self.AddDownloadTask(character, "", completeCallBack=self.LoadingHeadComplete, backParam=index)

    def AddNewChatItem(self, info, floor):
        title = info.get("title")
        description = info.get("description")
        level = info.get("minLevel")
        slogan = description
        character = ""
        url = info.get("icon", "")
        id = info.get("id")
        path = ""

        index = self.count()
        iwidget = CommentItemWidget(self)
        iwidget.index = index
        iwidget.setFocusPolicy(Qt.NoFocus)
        if isinstance(info.get("_comic"), dict):
            iwidget.linkId = info.get("_comic").get("_id")
            linkData = info.get("_comic").get("title", "")
            iwidget.linkLabel.setText("<u><font color=#d5577c>{}</font></u>".format(linkData))
            iwidget.linkLabel.setVisible(True)
            iwidget.killButton.setVisible(False)

        if isinstance(info.get("_game"), dict):
            iwidget.linkId = info.get("_game").get("_id")
            linkData = info.get("_game").get("title", "")
            iwidget.isGame = True
            iwidget.linkLabel.setText("GAME: <u><font color=#d5577c>{}</font></u>".format(linkData))
            iwidget.linkLabel.setVisible(True)
            iwidget.killButton.setVisible(False)

        if info.get("isLiked"):
            iwidget.SetLike()
        iwidget.starButton.hide()
        iwidget.commentButton.hide()
        iwidget.starButton.hide()

        # iwidget.commentLabel.setTextInteractionFlags(Qt.TextSelectableByKeyboard)
        iwidget.commentLabel.setTextInteractionFlags(Qt.NoTextInteraction)
        iwidget.setToolTip(slogan)
        iwidget.id = id
        iwidget.commentLabel.setText(description)
        iwidget.nameLabel.setText(title)
        # iwidget.commentButton.setText("({})".format(commentsCount))
        # iwidget.starButton.setText("({})".format(likesCount))
        iwidget.levelLabel.setText(" LV" + str(level) + " ")
        iwidget.titleLabel.setText(" " + title + " ")
        iwidget.url = ToolUtil.GetRealUrl(url, path)
        iwidget.path = path

        iwidget.character = character
        dayStr = ToolUtil.GetUpdateStr("")
        iwidget.dateLabel.setText(dayStr)
        iwidget.indexLabel.setText("{}".format(str(floor))+Str.GetStr(Str.Floor))
        iwidget.adjustSize()
        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.setItemWidget(item, iwidget)
        iwidget.PicLoad.connect(self.LoadingPicture)

    def LoadingPicture(self, index):
        item = self.item(index)
        widget = self.itemWidget(item)
        assert isinstance(widget, CommentItemWidget)
        self.AddDownloadTask(widget.url, widget.path, completeCallBack=self.LoadingPictureComplete, backParam=index)
        if "pica-web.wakamoment.tk" not in widget.character and widget.character and config.IsLoadingPicture:
            self.AddDownloadTask(widget.character, "", completeCallBack=self.LoadingHeadComplete, backParam=index)

    def AddUserKindItem(self, info, floor):
        content = info.get("slogan", "")
        name = info.get("name")
        avatar = info.get("avatar", {})
        commnetId = info.get('_id', "")
        title = info.get("title", "")
        level = info.get("level", 1)
        character = info.get("character", "")
        if not avatar:
            url = ""
            path = ""
        elif isinstance(avatar, str):
            url = avatar
            path = ""
        else:
            url = avatar.get("fileServer", "")
            path = avatar.get("path", "")

        index = self.count()
        iwidget = CommentItemWidget(self)
        iwidget.nameLabel.installEventFilter(iwidget)
        iwidget.setFocusPolicy(Qt.NoFocus)
        iwidget.killButton.hide()
        iwidget.nameLabel.setCursor(Qt.PointingHandCursor)
        iwidget.nameLabel.installEventFilter(iwidget)
        iwidget.setToolTip(info.get("slogan", ""))
        iwidget.id = commnetId
        iwidget.index = index
        iwidget.character = character
        iwidget.dateLabel.hide()
        iwidget.starButton.setCheckable(False)
        iwidget.commentButton.hide()
        iwidget.commentLabel.setText(content)
        iwidget.nameLabel.setText(name)
        iwidget.starButton.setText("({})".format(info.get('comicsUploaded')))
        iwidget.levelLabel.setText(" LV" + str(level) + " ")
        iwidget.titleLabel.setText(" " + title + " ")
        iwidget.url = ToolUtil.GetRealUrl(url, path)
        iwidget.path = ToolUtil.GetRealPath(commnetId, "user")

        iwidget.indexLabel.setText(Str.GetStr(Str.The)+"{}".format(str(floor)))
        iwidget.PicLoad.connect(self.LoadingPicture)
        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        self.setItemWidget(item, iwidget)

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetPicture(data)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetPictureErr(status)
        return

    def LoadingHeadComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetHeadData(data)
            pass
        else:
            pass
        return