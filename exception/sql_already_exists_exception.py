from exception.bilibili_exception import BilibiliException


class SqlAlreadyExistsException(BilibiliException):
    def __init__(self, msg) -> None:
        super().__init__(msg)
