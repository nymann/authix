from fastapi import Response
from pogo_api.endpoint import PostEndpoint

from authix.domain.authentication.service import AuthenticationService
from authix.endpoints.email_password_request import EmailPasswordRequest


class Login(PostEndpoint):
    def __init__(self, authentication_service: AuthenticationService) -> None:
        super().__init__()
        self._authentication_service = authentication_service

    async def endpoint(self, request: EmailPasswordRequest, response: Response) -> None:
        """Authenticate a user by creating a new refresh token, that can be used to create new JWTs."""
        auth_response = await self._authentication_service.authenticate(
            email=request.email,
            password=request.password.get_secret_value(),
        )
        response.set_cookie("refresh_token", auth_response.refresh_token, httponly=True, samesite="strict")
        response.headers["Authorization"] = f"JWT {auth_response.access_token}"
