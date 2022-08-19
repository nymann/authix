from fastapi import HTTPException
from fastapi import status

from auth_service.data.query_exceptions import UserAlreadyExistsError
from auth_service.data.users.queries.interface import UserQueries
from auth_service.domain.token.service import TokenService


class RegistrationService:
    def __init__(self, token_service: TokenService, user_queries: UserQueries) -> None:
        self._token_service = token_service
        self._user_queries = user_queries

    async def register(self, email: str, password: str) -> None:
        password_hash = self._token_service.get_password_hash(plain_password=password)
        try:
            await self._user_queries.add_user(email=email, password_hash=password_hash)
        except UserAlreadyExistsError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
