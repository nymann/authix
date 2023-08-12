from fastapi import Cookie
from pogo_api.endpoint import PostEndpoint

from authix.domain.authentication.service import AuthenticationService


class AccessToken(PostEndpoint):
    def __init__(self, authentication_service: AuthenticationService) -> None:
        super().__init__()
        self._authentication_service = authentication_service

    @property
    def path(self) -> str:
        return "/access_token"

    async def endpoint(self, refresh_token: str = Cookie(...)) -> str:
        """Create a new JWT access token from a refresh token."""
        return await self._authentication_service.create_access_token(refresh_token=refresh_token)
