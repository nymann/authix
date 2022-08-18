from datetime import datetime
from typing import Optional

from redis import StrictRedis

from auth_service.data.query_exceptions import QueryResultNotFoundError
from auth_service.data.revoke.revoke_queries import RevokeQueries


class RedisRevokeQueries(RevokeQueries):
    def __init__(self, **redis_args: str | int) -> None:
        self._redis = StrictRedis(**redis_args, encoding="utf-8", decode_responses=True)
        self._redis.ping()

    async def get(self, user_id: str) -> datetime:
        ts_isoformat: Optional[str] = self._redis.get(user_id)
        if ts_isoformat is None:
            raise QueryResultNotFoundError
        return datetime.fromisoformat(ts_isoformat)

    async def add(self, user_id: str, ts: datetime) -> None:
        self._redis.set(user_id, ts.isoformat())
