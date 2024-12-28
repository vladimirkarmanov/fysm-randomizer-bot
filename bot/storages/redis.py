import pickle
from functools import wraps
from typing import Any

import httpx
from redis.asyncio import ConnectionPool, Redis

from storages.base import BaseStorage


class RedisStorage(BaseStorage):
    excluded_types: list[Any] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = Redis(
            connection_pool=ConnectionPool(
                host=self.settings.REDIS_HOST,
                port=self.settings.REDIS_PORT,
                password=self.settings.REDIS_PASSWORD.get_secret_value(),
                decode_responses=True,
            )
        )

    async def hset(self, key: str, mapping: dict) -> int:
        return await self.redis.hset(key, mapping=mapping)

    async def hget(self, key: str) -> dict:
        return await self.redis.hgetall(key)

    async def set(self, key: str, value: int | str | bytes, ex: int | None = None):
        return await self.redis.set(key, value, ex=ex if ex else self.settings.REDIS_KEY_EX)

    async def get(self, key: str) -> str | bytes | None:
        return await self.redis.get(key)

    async def ttl(self, key: str) -> int:
        return await self.redis.ttl(key)

    async def delete(self, key: str) -> int:
        return await self.redis.delete(key)

    async def close(self):
        self.logger.info('Closing RedisStorage connection...')
        await self.redis.close()

    @staticmethod
    def _build_key(func, args: tuple, kwargs: dict) -> str:
        return f'{func.__module__}:{func.__name__}:{args}:{kwargs}'

    def cache(self, ex=None, self_=False):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if not self.settings.CACHE:
                    return await func(*args, **kwargs)
                if self_:
                    _args = args[1:]
                else:
                    _args = args
                cache_args = tuple(filter(lambda x: type(x) not in self.excluded_types, _args))
                cache_kwargs = {k: v for k, v in kwargs.items() if type(v) not in self.excluded_types}
                key = self._build_key(func, cache_args, cache_kwargs)
                byte_result = await self.get(key)

                if not byte_result:
                    result = await func(*args, **kwargs)

                    if isinstance(result, httpx.Response) and result.status_code >= 400:
                        self.logger.info('Skipping cache result of httpx.Response with response_code >=400')
                        return result

                    self.logger.info(f'Didn\'t find result for key="{key}". Creating')
                    byte_result = pickle.dumps(result)
                    await self.set(key, byte_result, ex=ex)
                    return result

                self.logger.info(f'Found cached result for key="{key}". Using it instead')
                return pickle.loads(byte_result)  # noqa

            return wrapper

        return decorator


redis_storage = RedisStorage()
