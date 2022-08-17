from datetime import datetime
from typing import Protocol


class RevokeQueries(Protocol):
    async def get(self, user_id: str) -> datetime:
        raise NotImplementedError()

    async def add(self, user_id: str, ts: datetime) -> None:
        raise NotImplementedError()
