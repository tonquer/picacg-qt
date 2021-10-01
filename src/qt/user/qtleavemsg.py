from src.server import req
from ui.qt_comment_list import QtCommentList


class QtLeaveMsg(QtCommentList):
    def __init__(self):
        QtCommentList.__init__(self)

        # self.commentButton.clicked.connect(self.SendComment)
        self.bookId = "5822a6e3ad7ede654696e482"
        self.InitReq(req.GetComments, req.SendComment, req.CommentsLikeReq, req.CommentsReportReq)

    def SwitchCurrent(self):
        self.loadingForm2.show()
        self.LoadComment()
        return
