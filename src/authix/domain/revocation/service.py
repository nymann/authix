from datetime import datetime
from datetime import timedelta
from datetime import timezone
import logging

from authix.data.refresh_token.queries.interface import RefreshQueries
from authix.data.revocation.queries.interface import RevokeQueries


class RevocationService:
    def __init__(
        self,
        revoke_queries: RevokeQueries,
        refresh_queries: RefreshQueries,
    ) -> None:
        self._revoke_queries = revoke_queries
        self._refresh_queries = refresh_queries

    async def revoke(self, refresh_token: str) -> None:
        user_id = await self._revoke_refresh_token(refresh_token=refresh_token)
        await self._broadcast_revocation_event(refresh_token=refresh_token, user_id=user_id)

    async def _revoke_refresh_token(self, refresh_token: str) -> str:
        user_id = str(await self._refresh_queries.delete(refresh_token=refresh_token))
        await self._revoke_queries.add(
            user_id=user_id,
            ts=datetime.now(tz=timezone.utc) + timedelta(minutes=5),
        )
        return user_id

    async def _broadcast_revocation_event(self, user_id: str, refresh_token: str) -> None:
        logging.info(f"{user_id} revoked their refresh_token ({refresh_token}")
