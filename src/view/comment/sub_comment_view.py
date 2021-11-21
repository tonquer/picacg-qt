from PySide6.QtWidgets import QWidget

from interface.ui_sub_comment import Ui_SubComment
from server import req


class SubCommentView(QWidget, Ui_SubComment):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_SubComment.__init__(self)
        self.setupUi(self)
        self.commentList.InitReq(req.GetCommentsChildrenReq, req.SendCommentChildrenReq, req.CommentsLikeReq, req.CommentsReportReq)

    def SwitchCurrent(self, **kwargs):
        return self.commentList.SwitchCurrent(**kwargs)

    def SetWidget(self, widget):
        self.comment.starButton.hide()
        self.comment.commentButton.hide()
        self.comment.indexLabel.setText(widget.indexLabel.text())
        self.comment.dateLabel.setText(widget.dateLabel.text())
        self.comment.titleLabel.setText(widget.titleLabel.text())
        self.comment.nameLabel.setText(widget.nameLabel.text())
        self.comment.picIcon.setPixmap(widget.picIcon.pixmap())
        self.comment.commentLabel.setText(widget.commentLabel.text())
        self.comment.levelLabel.setText(widget.levelLabel.text())