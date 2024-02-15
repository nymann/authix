from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from authix.version import __version__


class PasswordConfig(BaseModel):
    min_length: int
    max_length: int
    symbols: str
    min_special_chars: int
    min_lowercase_chars: int
    min_uppercase_chars: int
    min_digits: int


class RevocationConfig(BaseModel):
    kafka_host: str
    kafka_port: str
    kafka_topic: str

    def bootstrap_servers(self) -> str:
        return f"{self.kafka_host}:{self.kafka_port}"


class AuthConfig(BaseSettings):
    auth_title: str
    key_folder: Path
    log_level: str
    mongodb_url: str
    password: PasswordConfig
    refresh_redis: str
    revocation: Optional[RevocationConfig] = None
    version: str = __version__

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )
