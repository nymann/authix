import asyncio
import logging

from authix.core.config import RevocationConfig
from authix.data.query_exceptions import QueryResultNotFoundError
from authix.data.refresh_token.refresh_token_queries import RefreshQueries
from authix.domain.device_id import generate_device_id
from authix.domain.domain_exceptions import Unauthorized
from authix.domain.revocation.event import RevocationEvent
from authix.domain.revocation.publisher import RevocationPublisher


class RevocationService:
    def __init__(self, refresh_queries: RefreshQueries, config: RevocationConfig) -> None:
        self._refresh_queries = refresh_queries
        self._publisher = RevocationPublisher(config=config)

    async def revoke(self, refresh_token: str) -> None:
        try:
            revocation_event = await self._revoke_refresh_token(refresh_token=refresh_token)
        except QueryResultNotFoundError:
            raise Unauthorized
        asyncio.create_task(self._publisher.publish_and_forget(revocation_event=revocation_event))

    async def _revoke_refresh_token(self, refresh_token: str) -> RevocationEvent:
        device_id = generate_device_id(refresh_token=refresh_token)
        user_id = await self._refresh_queries.delete(refresh_token=refresh_token)
        logging.debug("user.id '%s' revoked refresh_token '%s', for device '%s'.", user_id, refresh_token, device_id)
        return RevocationEvent(user_id=user_id, device_id=device_id)
