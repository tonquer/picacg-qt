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

    UnderReviewBook = Str.UnderReviewBook

