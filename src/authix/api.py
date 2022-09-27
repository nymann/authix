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
        self.api = FastAPI(version=config.version, title=config.auth_title, docs_url="/")
        self.services = service_container
        self.add_endpoints()

    @property
    def endpoints(self) -> list[Endpoint]:
        return [
            CreateAccessToken(authentication_service=self.services.authentication_service()),
            Login(authentication_service=self.services.authentication_service()),
            Logout(revocation_service=self.services.revocation_service()),
            PublicKey(key_service=self.services.key_service()),
            Register(registration_service=self.services.registration_service()),
        ]

    def add_endpoints(self) -> None:
        for endpoint in self.endpoints:
            endpoint.route.add_to_router(self.api)
