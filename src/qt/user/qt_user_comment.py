from src.server import req
from ui.qt_comment_list import QtCommentList


class QtUserComment(QtCommentList):
    def __init__(self):
        QtCommentList.__init__(self)
        self.commentButton.hide()
        self.commentLine.hide()
        self.InitReq(req.GetUserCommentReq, req.SendComment, req.CommentsLikeReq, req.CommentsReportReq)

    def SwitchCurrent(self):
        self.loadingForm2.show()
        self.LoadComment()
        return
