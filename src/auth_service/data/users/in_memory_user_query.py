from typing import Iterable

from pydantic import UUID4

from auth_service.data.query_exceptions import QueryResultNotFoundError
from auth_service.data.users.user_model import UserModel
from auth_service.data.users.user_queries import UserQueries


class InMemoryUserQueries(UserQueries):
    def __init__(self, seeded_users: Iterable[UserModel]) -> None:
        self._users: dict[UUID4, UserModel] = {}
        self._email_lookup: dict[str, UserModel] = {}
        for user in seeded_users:
            self._users[user.id] = user
            self._email_lookup[user.email] = user

    async def get_user_by_id(self, user_id: UUID4) -> UserModel:
        try:
            return self._users[user_id]
        except KeyError as error:
            raise QueryResultNotFoundError from error

    async def ger_user_by_email(self, email: str) -> UserModel:
        try:
            return self._email_lookup[email]
        except KeyError as error:
            raise QueryResultNotFoundError from error
