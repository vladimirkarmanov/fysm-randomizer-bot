import functools
import uuid
from asyncio import shield

from httpx import AsyncClient, HTTPError

from core.deps import get_logger
from errors.exceptions import InternalServerError, NotFound

logger = get_logger()


def with_client(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        client = AsyncClient()
        xid = uuid.uuid4()
        try:
            result = await func(*args, **kwargs, client=client)
        except HTTPError as exc:
            logger.error(f"[{xid}] HTTP Exception for {exc.request.url} - {exc};")
            raise
        except Exception as exc:
            logger.error(f"[{xid}] HTTP Exception; ({exc})")
            raise
        finally:
            if client:
                await shield(client.aclose())
                logger.debug(f"[{xid}] HTTP client closed")
        return result

    return wrapped


@with_client
async def get(url: str, params: dict = None, format: str = 'json', *, client: AsyncClient) -> dict | str | bytes:
    if not params:
        params = {}
    logger.debug(f"Send request to {url}")
    r = await client.get(url, params=params)
    if r.status_code == 500:
        raise InternalServerError
    if r.status_code == 404:
        raise NotFound

    if format == 'json':
        return r.json()
    elif format == 'text':
        return r.text
    elif format == 'bytes':
        return r.read()
