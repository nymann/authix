import logging

from pydantic import UUID4

from authix.core.config import RevocationConfig
from authix.data.query_exceptions import QueryResultNotFoundError
from authix.data.refresh_token.refresh_token_queries import RefreshQueries
from authix.domain.domain_exceptions import Unauthorized
from authix.domain.revocation.event import RevocationEvent
from authix.domain.revocation.publisher import RevocationPublisher


class RevocationService:
    def __init__(self, refresh_queries: RefreshQueries, config: RevocationConfig) -> None:
        self._refresh_queries = refresh_queries
        self._publisher = RevocationPublisher(config=config)

    async def revoke(self, refresh_token: str) -> None:
        try:
            user_id = await self._revoke_refresh_token(refresh_token=refresh_token)
        except QueryResultNotFoundError:
            raise Unauthorized
        logging.debug(f"{user_id} revoked their refresh_token ({refresh_token})")
        event = RevocationEvent(user_id=user_id)
        await self._publisher.publish(revocation_event=event)

    async def _revoke_refresh_token(self, refresh_token: str) -> UUID4:
        return await self._refresh_queries.delete(refresh_token=refresh_token)
