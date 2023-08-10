from authix.api import AuthService
from authix.core.config import AuthConfig
from authix.core.service_container import ServiceContainer

config = AuthConfig()  # type: ignore
service_container = ServiceContainer(config=config)
api = AuthService(config=config, service_container=service_container).api
