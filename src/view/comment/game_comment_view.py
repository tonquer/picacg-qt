from component.widget.comment_widget import CommentWidget
from server import req


class GameCommentView(CommentWidget):
    def __init__(self, parent=None):
        CommentWidget.__init__(self, parent)
        self.InitReq(req.GetGameCommentsReq, req.SendGameCommentsReq, req.GameCommentsLikeReq, req.CommentsReportReq)