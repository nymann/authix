from pathlib import Path

from pydantic import BaseSettings
from pydantic import RedisDsn

from authix import version


class AuthSettings(BaseSettings):
    auth_title: str
    client_redis: RedisDsn
    refresh_redis: RedisDsn
    key_folder: Path

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class AuthConfig:
    def __init__(self) -> None:
        self.version: str = version.__version__
        self.settings: AuthSettings = AuthSettings()
