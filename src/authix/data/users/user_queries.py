from abc import ABC
from abc import abstractmethod

from pydantic import UUID4

from authix.data.users.model import UserModel


class UserQueries(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserModel:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID4) -> UserModel:
        raise NotImplementedError()

    @abstractmethod
    async def add_user(self, email: str, password_hash: str) -> UserModel:
        raise NotImplementedError()
