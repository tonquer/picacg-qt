from tools.str import Str


class Status(object):
    Ok = Str.Ok
    Load = Str.Load
    Error = Str.Error
    WaitLoad = Str.WaitLoad
    NetError = Str.NetError
    UserError = Str.UserError
    RegisterError = Str.RegisterError
    UnKnowError = Str.UnKnowError
    NotFoundBook = Str.NotFoundBook
    ParseError = Str.ParseError
    NeedGoogle = Str.NeedGoogle
    SetHeadError = Str.SetHeadError
    TimeOut = Str.TimeOut
    SSLErr = Str.SSLErr
    ResetErr = Str.ResetErr
    ConnectErr = Str.ConnectErr
    ProxyError = Str.ProxyError
    DownloadFail = Str.DownloadFail
    OfflineModel = Str.OfflineModel

    UnderReviewBook = Str.UnderReviewBook
    SaveError = Str.SaveError
    AddError = Str.AddError
    FileError = Str.FileError
    PathError = Str.PathError
    FileFormatError = Str.FileFormatError

