from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem

from component.list.base_list_widget import BaseListWidget
from component.widget.comment_item_widget import CommentItemWidget
from config import config
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class UserListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.resize(800, 600)
        # self.setMinimumHeight(400)
        # self.setFrameShape(self.NoFrame)  # 无边框
        self.setFlow(self.TopToBottom)
        # self.setWrapping(True)
        # self.setResizeMode(self.Adjust)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.SelectMenuBook)
        # self.doubleClicked.connect(self.OpenBookInfo)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
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
        else:
            user = info.get("_user", {})
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
        iwidget.url = url
        iwidget.path = path
        dayStr = ToolUtil.GetUpdateStr(createdTime)
        iwidget.dateLabel.setText(dayStr)
        iwidget.indexLabel.setText("{}".format(str(floor))+Str.GetStr(Str.Floor))
        iwidget.adjustSize()
        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.setItemWidget(item, iwidget)
        if url and config.IsLoadingPicture:
            self.AddDownloadTask(url, path, None, self.LoadingPictureComplete, True, index, True)
        if "pica-web.wakamoment.tk" not in character and character and config.IsLoadingPicture:
            self.AddDownloadTask(character, "", None, self.LoadingHeadComplete, True, index, True)

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
        iwidget.setFocusPolicy(Qt.NoFocus)
        iwidget.killButton.hide()
        iwidget.nameLabel.setCursor(Qt.PointingHandCursor)
        iwidget.nameLabel.installEventFilter(iwidget)
        iwidget.setToolTip(info.get("slogan", ""))
        iwidget.id = commnetId
        iwidget.dateLabel.hide()
        iwidget.starButton.setCheckable(False)
        iwidget.commentButton.hide()
        iwidget.commentLabel.setText(content)
        iwidget.nameLabel.setText(name)
        iwidget.starButton.setText("({})".format(info.get('comicsUploaded')))
        iwidget.levelLabel.setText(" LV" + str(level) + " ")
        iwidget.titleLabel.setText(" " + title + " ")
        iwidget.url = url
        iwidget.path = path
        iwidget.indexLabel.setText(Str.GetStr(Str.The)+"{}".format(str(floor)))

        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        self.setItemWidget(item, iwidget)
        if url and config.IsLoadingPicture:
            self.AddDownloadTask(url, path, None, self.LoadingPictureComplete, True, index, True)
        if "pica-web.wakamoment.tk" not in character and config.IsLoadingPicture:
            self.AddDownloadTask(character, "", None, self.LoadingHeadComplete, True, index, True)

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetPicture(data)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetPictureErr()
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