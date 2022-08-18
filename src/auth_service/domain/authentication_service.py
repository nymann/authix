from datetime import datetime
from datetime import timezone
from typing import Any
from uuid import uuid4

from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel

from auth_service.data.query_exceptions import QueryResultNotFoundError
from auth_service.data.refresh.refresh_queries import RefreshQueries
from auth_service.data.revoke.revoke_queries import RevokeQueries
from auth_service.data.users.user_queries import UserQueries
from auth_service.domain.token_service import TokenService


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str


class AuthenticationService:
    def __init__(
        self,
        user_queries: UserQueries,
        revoke_queries: RevokeQueries,
        refresh_queries: RefreshQueries,
        token_service: TokenService,
    ) -> None:
        self._user_queries = user_queries
        self._revoke_queries = revoke_queries
        self._refresh_queries = refresh_queries
        self._token_service = token_service

    async def authenticate(self, email: str, password: str) -> AuthResponse:
        try:
            user = await self._user_queries.ger_user_by_email(email=email)
        except QueryResultNotFoundError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if not self._token_service.verify_password(plain_password=password, hashed_password=user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        refresh_token = str(uuid4())
        await self._refresh_queries.add(refresh_token=refresh_token, user_id=user.id)
        access_token = self._token_service.create_access_token(user=user)
        return AuthResponse(access_token=access_token, refresh_token=refresh_token)

    async def create_access_token(self, refresh_token: str) -> str:
        user_id = await self._refresh_queries.get_user_id(refresh_token=refresh_token)
        user = await self._user_queries.get_user_by_id(user_id=user_id)
        return self._token_service.create_access_token(user=user)

    async def client_implementation(self, access_token: str) -> dict[str, Any]:
        decoded_data: dict[str, Any] = self._token_service.decode(access_token=access_token)
        user_id: str = decoded_data["id"]
        try:
            revoked_dt = await self._revoke_queries.get(user_id=user_id)
        except QueryResultNotFoundError:
            return decoded_data
        exp: datetime = datetime.fromtimestamp(decoded_data["exp"], tz=timezone.utc)
        if exp < revoked_dt:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Revoked token")
        return decoded_data
