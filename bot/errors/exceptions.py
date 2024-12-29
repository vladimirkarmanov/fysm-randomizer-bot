class InnerException(Exception):
    msg: str


class NotFound(InnerException):
    msg = 'Не найдено'


class InternalServerError(InnerException):
    msg = 'Что-то пошло не так'
