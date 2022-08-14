from component.widget.comment_widget import CommentWidget
from server import req


class FriedCommentView(CommentWidget):
    def __init__(self, parent=None):
        CommentWidget.__init__(self, parent)
        self.InitReq(req.AppCommentInfoReq, req.AppSendCommentInfoReq, req.AppCommentLikeReq, req.CommentsReportReq)