from typing import Protocol

from pydantic import UUID4

from authix.data.users.model import UserModel


class UserQueries(Protocol):
    async def ger_user_by_email(self, email: str) -> UserModel:
        raise NotImplementedError()

    async def get_user_by_id(self, user_id: UUID4) -> UserModel:
        raise NotImplementedError()

    async def add_user(self, email: str, password_hash: str) -> UserModel:
        raise NotImplementedError()
