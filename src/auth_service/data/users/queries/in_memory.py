from uuid import uuid4

from pydantic import UUID4

from auth_service.data.query_exceptions import QueryResultNotFoundError
from auth_service.data.query_exceptions import UserAlreadyExistsError
from auth_service.data.users.model import UserModel
from auth_service.data.users.queries.interface import UserQueries


class InMemoryUserQueries(UserQueries):
    def __init__(self) -> None:
        self._users: dict[UUID4, UserModel] = {}
        self._email_lookup: dict[str, UserModel] = {}

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

    async def add_user(self, email: str, password_hash: str) -> UserModel:
        if email in self._email_lookup:
            raise UserAlreadyExistsError()
        user = UserModel(
            id=uuid4(),
            email=email,
            password_hash=password_hash,
        )
        self._users[user.id] = user
        self._email_lookup[user.email] = user
        return user
