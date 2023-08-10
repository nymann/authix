from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from authix.version import __version__


class AuthConfig(BaseSettings):
    auth_title: str
    client_redis: str
    refresh_redis: str
    key_folder: Path
    mongodb_url: str
    min_password_length: int
    max_password_length: int
    password_symbols: str
    min_number_of_special_chars: int
    min_number_of_lowercase_chars: int
    min_number_of_uppercase_chars: int
    min_number_of_digits: int
    version: str = __version__

    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")  # type:ignore
