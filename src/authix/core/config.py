from pathlib import Path

from pydantic import BaseSettings
from pydantic import RedisDsn

from authix.version import __version__


class AuthConfig(BaseSettings):
    auth_title: str
    client_redis: RedisDsn
    refresh_redis: RedisDsn
    key_folder: Path
    mongodb_url: str
    version: str = __version__

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
