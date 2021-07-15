from src.util import ToolUtil


class BaseRes(object):
    def __init__(self, data, isParseRes) -> None:
        super().__init__()
        self.raw = data
        self.data = {}
        self.code = 0
        self.message = ""
        self.reqBak = None
        if isParseRes:
            ToolUtil.ParseFromData(self, self.GetText())

    def GetText(self):
        if hasattr(self.raw, "text"):
            return self.raw.text
        return ""
