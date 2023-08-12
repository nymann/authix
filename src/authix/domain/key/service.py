from jwt import AbstractJWKBase
from jwt import jwk_from_pem

from authix.core.config import AuthConfig


class KeyService:
    def __init__(self, config: AuthConfig) -> None:
        self._key_folder = config.key_folder
        self._private_key = self._read_key(name="private.pem")
        self._public_key = self._read_key(name="public.pem")

    def get_private_key(self) -> AbstractJWKBase:
        return jwk_from_pem(self._private_key)

    def get_public_key(self) -> bytes:
        return self._public_key

    def _read_key(self, name: str) -> bytes:
        key_path = self._key_folder.joinpath(name)
        with open(file=key_path, mode="rb") as key:
            return key.read()
