from app.interfaces.uow import IUnitOfWork


class IoC:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
