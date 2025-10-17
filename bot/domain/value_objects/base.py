from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """This method checks that a value is valid to create this value object"""
        pass


@dataclass(frozen=True)
class ValueObject(BaseValueObject, Generic[T]):
    value: T

    def to_raw(self) -> T:
        return self.value
