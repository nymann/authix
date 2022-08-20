from fastapi import FastAPI

from authix.core.config import AuthConfig
from authix.router import auth_router


class AuthService:
    def __init__(self, config: AuthConfig) -> None:
        self.api = FastAPI(version=config.version, title=config.settings.auth_title, docs_url="/")
        self.api.include_router(router=auth_router)
