import logging

from authix.data.query_exceptions import QueryResultNotFoundError
from authix.data.refresh_token.refresh_token_queries import RefreshQueries
from authix.domain.domain_exceptions import Unauthorized


class RevocationService:
    def __init__(self, refresh_queries: RefreshQueries) -> None:
        self._refresh_queries = refresh_queries

    async def revoke(self, refresh_token: str) -> None:
        try:
            user_id = await self._revoke_refresh_token(refresh_token=refresh_token)
        except QueryResultNotFoundError:
            raise Unauthorized
        await self._broadcast_revocation_event(refresh_token=refresh_token, user_id=user_id)

    async def _revoke_refresh_token(self, refresh_token: str) -> str:
        return str(await self._refresh_queries.delete(refresh_token=refresh_token))

    async def _broadcast_revocation_event(self, user_id: str, refresh_token: str) -> None:
        logging.info(f"{user_id} revoked their refresh_token ({refresh_token}")
