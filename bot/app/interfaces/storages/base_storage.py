from abc import ABC, abstractmethod


class IBaseStorage(ABC):
    @abstractmethod
    def get(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError
