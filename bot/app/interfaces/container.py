from contextlib import contextmanager
from typing import Any, Callable, Iterator, Protocol, Type, runtime_checkable

from infra.config.settings import get_settings

settings = get_settings()


@runtime_checkable
class DIProtocol(Protocol):
    def register(self, key: str, factory: Callable[[], Any], **kwargs) -> None: ...
    def resolve(self, key: str) -> Any: ...
    @contextmanager
    def override(self, key: str, new_obj: Callable[[], Any], **kwargs) -> Iterator[None]: ...
    def lazy_import(self, module_path: str, class_name: str) -> Callable[[], Type]: ...
