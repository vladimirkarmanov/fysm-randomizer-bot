import punq

from storages.base import BaseStorage
from storages.redis import RedisStorage

container = punq.Container()

container.register(BaseStorage, instance=RedisStorage())
