import threading
from contextlib import contextmanager
from types import LambdaType
from typing import Any, Callable, Iterator, Protocol, Type

from infra.config.settings import get_settings

settings = get_settings()


class DIProtocol(Protocol):
    """DI interface for type hints."""

    def register(self, key: str, factory: Callable[[], Any], **kwargs) -> None: ...
    def resolve(self, key: str) -> Any: ...
    @contextmanager
    def override(self, key: str, new_obj: Callable[[], Any], **kwargs) -> Iterator[None]: ...
    def lazy_import(self, module_path: str, class_name: str) -> Callable[[], Type]: ...


class _DIItem:
    _item: Callable[[], Any]
    _options: dict

    _default_options = {'call': True}

    def __init__(self, item: Callable[[], Any], options: dict) -> None:
        self._item = item
        self._options = {**self._default_options, **options}

    def get_value(self):
        return self._item() if self._options.get('call') and isinstance(self._item, LambdaType) else self._item


class _DI:
    def __init__(self):
        self._container: dict[str, _DIItem] = {}
        self._lock = threading.Lock()
        self._initialized = False

    def initialize(self):
        raise NotImplementedError

    def _initialize(self):
        """Initialize container once with thread safety."""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self.initialize()
                    self._initialized = True

    def register(self, key: str, factory: Callable[[], Any], **kwargs):
        self._register_item(key, _DIItem(factory, kwargs))

    def _register_item(self, key: str, item: _DIItem):
        self._container[key] = item

    def resolve(self, key: str) -> Any:
        self._initialize()
        return self._resolve_item(key).get_value()

    def _resolve_item(self, key: str) -> _DIItem:
        if key not in self._container:
            raise AttributeError(f'Nothing registered with the key "{key}"')
        return self._container[key]

    @contextmanager
    def override(self, key: str, new_obj: Callable[[], Any], **kwargs) -> Iterator[None]:
        self._initialize()
        existing_item = self._resolve_item(key)
        self._register_item(key, _DIItem(new_obj, kwargs))
        try:
            yield
        finally:
            self._register_item(key, existing_item)

    def lazy_import(self, module_path: str, class_name: str) -> Callable[[], Type]:
        """Lazy import a class from a module."""
        return lambda: self._import(module_path, class_name)

    def _import(self, module_path: str, class_name: str) -> Type:
        """Dynamically import a class from a module."""
        module = __import__(module_path, fromlist=[class_name])
        return getattr(module, class_name)


class _Container(_DI):
    def initialize(self) -> None:
        # Database session factory
        self.register('session_factory', self.lazy_import('infra.db.main', 'async_session_factory'))

        # UnitOfWork
        self.register('uow_cls', self.lazy_import('infra.db.uow', 'SqlAlchemyUnitOfWork'))

        # Redis storage
        self.register('redis_storage_cls', self.lazy_import('infra.storage', 'RedisStorage'))


container: DIProtocol = _Container()

__all__ = ['DIProtocol', 'container']
