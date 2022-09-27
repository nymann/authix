from fastapi import Cookie
from pogo_api.endpoint import DeleteEndpoint

from authix.domain.revocation.service import RevocationService


class Logout(DeleteEndpoint):
    def __init__(self, revocation_service: RevocationService) -> None:
        super().__init__()
        self._revocation_service = revocation_service

    async def endpoint(self, refresh_token: str = Cookie(default=...)) -> None:
        """Log a user out by deleting their refresh token, and broadcasting a revoke event."""
        return await self._revocation_service.revoke(refresh_token=refresh_token)
