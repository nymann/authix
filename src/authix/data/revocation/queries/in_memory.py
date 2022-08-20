from datetime import datetime

from authix.data.query_exceptions import QueryResultNotFoundError
from authix.data.revoke.revoke_queries import RevokeQueries


class InMemoryRevokeQueries(RevokeQueries):
    def __init__(self) -> None:
        self.revoked: dict[str, datetime] = {}

    async def get(self, user_id: str) -> datetime:
        try:
            return self.revoked[user_id]
        except KeyError as error:
            raise QueryResultNotFoundError from error

    async def add(self, user_id: str, ts: datetime) -> None:
        self.revoked[user_id] = ts
