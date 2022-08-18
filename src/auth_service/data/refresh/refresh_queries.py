from typing import Protocol

from pydantic import UUID4


class RefreshQueries(Protocol):
    async def get_user_id(self, refresh_token: str) -> UUID4:
        raise NotImplementedError()

    async def add(self, refresh_token: str, user_id: UUID4) -> None:
        raise NotImplementedError()

    async def delete(self, refresh_token: str) -> UUID4:
        raise NotImplementedError()
