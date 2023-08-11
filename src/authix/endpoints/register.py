from pogo_api.endpoint import PostEndpoint

from authix.domain.registration.service import RegistrationService
from authix.endpoints.email_password_request import EmailPasswordRequest


class Register(PostEndpoint):
    def __init__(self, registration_service: RegistrationService) -> None:
        super().__init__()
        self._registration_service = registration_service

    async def endpoint(self, request: EmailPasswordRequest) -> None:
        return await self._registration_service.register(
            email=request.email,
            password=request.password.get_secret_value(),
        )
