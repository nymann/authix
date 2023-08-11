import logging

from fastapi import FastAPI
from pogo_api.endpoint import Endpoint

from authix.core.config import AuthConfig
from authix.core.service_container import ServiceContainer
from authix.endpoints.create_access_token import CreateAccessToken
from authix.endpoints.login import Login
from authix.endpoints.logout import Logout
from authix.endpoints.public_key import PublicKey
from authix.endpoints.register import Register


class AuthService:
    def __init__(self, config: AuthConfig, service_container: ServiceContainer) -> None:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s:\t%(asctime)s\t%(message)s")  # noqa: WPS323
        self.api = FastAPI(version=config.version, title=config.auth_title, docs_url="/")
        self._services = service_container
        self._add_endpoints_to_api()

    def _get_endpoints(self) -> list[Endpoint]:
        return [
            CreateAccessToken(authentication_service=self._services.authentication_service()),
            Login(authentication_service=self._services.authentication_service()),
            Logout(revocation_service=self._services.revocation_service()),
            PublicKey(key_service=self._services.key_service()),
            Register(registration_service=self._services.registration_service()),
        ]

    def _add_endpoints_to_api(self) -> None:
        for endpoint in self._get_endpoints():
            endpoint.route.add_to_router(self.api)
