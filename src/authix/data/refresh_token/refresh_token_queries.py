from abc import ABC
from abc import abstractmethod

from pydantic import UUID4


class RefreshQueries(ABC):
    @abstractmethod
    async def get_user_id(self, refresh_token: str) -> UUID4:
        raise NotImplementedError()

    @abstractmethod
    async def add(self, refresh_token: str, user_id: UUID4) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, refresh_token: str) -> UUID4:
        raise NotImplementedError()
