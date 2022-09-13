from uuid import uuid4

from pydantic import BaseModel

from authix.data.query_exceptions import QueryResultNotFoundError
from authix.data.refresh_token.queries.interface import RefreshQueries
from authix.data.users.queries.interface import UserQueries
from authix.domain.domain_exceptions import Unauthorized
from authix.domain.token.service import TokenService


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str


class AuthenticationService:
    def __init__(
        self,
        user_queries: UserQueries,
        refresh_queries: RefreshQueries,
        token_service: TokenService,
    ) -> None:
        self._user_queries = user_queries
        self._refresh_queries = refresh_queries
        self._token_service = token_service

    async def authenticate(self, email: str, password: str) -> AuthResponse:
        try:
            user = await self._user_queries.get_user_by_email(email=email)
        except QueryResultNotFoundError:
            raise Unauthorized

        if not self._token_service.verify_password(plain_password=password, hashed_password=user.password_hash):
            raise Unauthorized

        refresh_token = str(uuid4())
        await self._refresh_queries.add(refresh_token=refresh_token, user_id=user.id)
        access_token = self._token_service.create_access_token(user=user)
        return AuthResponse(access_token=access_token, refresh_token=refresh_token)

    async def create_access_token(self, refresh_token: str) -> str:
        try:
            user_id = await self._refresh_queries.get_user_id(refresh_token=refresh_token)
        except QueryResultNotFoundError:
            raise Unauthorized
        try:
            user = await self._user_queries.get_user_by_id(user_id=user_id)
        except QueryResultNotFoundError:
            raise Unauthorized
        return self._token_service.create_access_token(user=user)
