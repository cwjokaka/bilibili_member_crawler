from exception.bilibili_error import BilibiliError


class RequestError(BilibiliError):
    def __init__(self, msg) -> None:
        super().__init__(msg)
