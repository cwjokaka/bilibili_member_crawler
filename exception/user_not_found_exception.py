from exception.bilibili_exception import BilibiliException


class UserNotFoundException(BilibiliException):
    def __init__(self, msg) -> None:
        super().__init__(msg)
