class InnerException(Exception):
    msg = None


class NotFound(InnerException):
    msg = 'Не найдено'


class InternalServerError(InnerException):
    msg = 'Что-то пошло не так'
