from component.widget.comment_widget import CommentWidget
from server import req


class CommentView(CommentWidget):
    def __init__(self, parent=None):
        CommentWidget.__init__(self, parent)
        self.InitReq(req.GetCommentsReq, req.SendCommentReq, req.CommentsLikeReq, req.CommentsReportReq)