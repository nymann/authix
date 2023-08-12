from pogo_api.endpoint import GetEndpoint

from authix.domain.key.service import KeyService


class PublicKey(GetEndpoint):
    def __init__(self, key_service: KeyService) -> None:
        super().__init__()
        self._key_service = key_service

    @property
    def path(self) -> str:
        return "/public_key"

    async def endpoint(self) -> str:
        return self._key_service.get_public_key().decode()
