from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.status import Status
from tools.str import Str


class ReadProxy(QtTaskBase):
    def __init__(self):
        QtTaskBase.__init__(self)
        self.bookId = 0
        self.epsId = 0
        self.maxPic = 0
        self.curIndex = 0
        self.pageIndex = 0
        self.epsName = ""
        self.initCallBack = None
        return

    def Init(self):
        self.AddDownloadBook(self.bookId, self.epsId, 0, statusBack=self.InitBack, backParam=0, isInit=True)
        return

    def InitBack(self, raw):
        st = raw["st"]
        if st == Status.Error:
            QtOwner().ShowError(Str.GetStr(st))
            return
        maxPic = raw.get("maxPic")
        if not maxPic or self.maxPic > 0:
            return
        self.maxPic = maxPic
        title = raw.get("title", "")
        self.epsName = title
        # info = BookMgr().GetBook(self.bookId)
        if 0 < self.pageIndex < self.maxPic:
            self.curIndex = self.pageIndex
            QtOwner().ShowMsg(Str.GetStr(Str.ContinueRead) + str(self.pageIndex + 1) + Str.GetStr(Str.Page))
        self.AddHistory()
        self.initCallBack()
        self.scrollArea.InitAllQLabel(self.maxPic, self.curIndex)
        self.qtTool.UpdateSlider()
        self.CheckLoadPicture()
        self.qtTool.InitSlider(self.maxPic)
        return

    def AddHistory(self):
        bookName = QtOwner().bookInfoView.bookName
        url = QtOwner().bookInfoView.url
        path = QtOwner().bookInfoView.path
        QtOwner().historyView.AddHistory(self.bookId, bookName, self.epsId, self.curIndex, url, path)
        return