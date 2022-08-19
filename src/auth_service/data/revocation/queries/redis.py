from datetime import datetime
from typing import Optional

from pydantic import RedisDsn
from redis import StrictRedis

from auth_service.data.query_exceptions import QueryResultNotFoundError
from auth_service.data.revocation.queries.interface import RevokeQueries


class RedisRevokeQueries(RevokeQueries):
    def __init__(self, dsn: RedisDsn) -> None:
        self._redis = StrictRedis.from_url(url=dsn, encoding="utf-8", decode_responses=True)

    async def get(self, user_id: str) -> datetime:
        ts_isoformat: Optional[str] = self._redis.get(user_id)
        if ts_isoformat is None:
            raise QueryResultNotFoundError
        return datetime.fromisoformat(ts_isoformat)

    async def add(self, user_id: str, ts: datetime) -> None:
        self._redis.set(user_id, ts.isoformat())
