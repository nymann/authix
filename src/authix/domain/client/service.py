from datetime import datetime
from datetime import timezone
from typing import Any

from fastapi import HTTPException
from fastapi import status

from authix.data.query_exceptions import QueryResultNotFoundError
from authix.data.revocation.queries.interface import RevokeQueries
from authix.domain.token.service import TokenService


class ClientImplementationService:
    def __init__(
        self,
        revoke_queries: RevokeQueries,
        token_service: TokenService,
    ) -> None:
        self._revoke_queries = revoke_queries
        self._token_service = token_service

    async def client_implementation(self, access_token: str) -> dict[str, Any]:
        decoded_data: dict[str, Any] = self._token_service.decode(access_token=access_token)
        user_id: str = decoded_data["id"]
        try:
            revoked_dt = await self._revoke_queries.get(user_id=user_id)
        except QueryResultNotFoundError:
            return decoded_data
        if self._is_revoked(exp=decoded_data["exp"], revoked_dt=revoked_dt):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Revoked token")
        return decoded_data

    def _is_revoked(self, exp: int, revoked_dt: datetime) -> bool:
        return datetime.fromtimestamp(exp, tz=timezone.utc) < revoked_dt
