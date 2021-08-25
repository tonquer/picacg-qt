from conf import config
from src.util import ToolUtil


class BaseRes(object):
    def __init__(self, data, isParseRes) -> None:
        super().__init__()
        self.raw = data
        self.data = {}
        self.code = 0
        self.message = ""
        self.reqBak = None
        self.isParseRes = isParseRes
        if isParseRes:
            ToolUtil.ParseFromData(self, self.GetText())

    def __str__(self):
        if config.LogIndex == 0:
            return ""
        if self.isParseRes:
            data = self.GetText()
        else:
            data = ""
        return "code:{}, raw:{}".format(self.code, data.replace("\n", ""))

    def GetText(self):
        if hasattr(self.raw, "text"):
            return self.raw.text
        return ""
