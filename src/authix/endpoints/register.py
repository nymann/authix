from pogo_api.endpoint import PostEndpoint

from authix.domain.registration.service import RegistrationService


class Register(PostEndpoint):
    def __init__(self, registration_service: RegistrationService) -> None:
        super().__init__()
        self._registration_service = registration_service

    async def endpoint(self, email: str, password: str) -> None:
        return await self._registration_service.register(email=email, password=password)
