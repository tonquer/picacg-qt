from component.widget.comment_widget import CommentWidget
from server import req


class MyCommentView(CommentWidget):
    def __init__(self, parent=None):
        CommentWidget.__init__(self, parent)
        self.InitReq(req.GetUserCommentReq, req.SendCommentReq, req.CommentsLikeReq, req.CommentsReportReq)
        self.pushButton.hide()
        self.commentLine.hide()