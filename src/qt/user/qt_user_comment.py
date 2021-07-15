from src.server import req
from ui.qt_comment_list import QtCommentList


class QtUserComment(QtCommentList):
    def __init__(self):
        QtCommentList.__init__(self)
        self.InitReq(req.GetUserCommentReq, req.SendComment, req.CommentsLikeReq)

    def SwitchCurrent(self):
        self.loadingForm2.show()
        self.LoadComment()
        return
