from pydantic import BaseSettings
from pydantic import SecretStr

from auth_service import version


class AuthSettings(BaseSettings):
    auth_title: str
    secret: SecretStr
    client_redis_password: SecretStr
    client_redis_port: int
    refresh_redis_password: SecretStr
    refresh_redis_port: int = 6379

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class AuthConfig:
    def __init__(self) -> None:
        self.version: str = version.__version__
        self.settings: AuthSettings = AuthSettings()
