from authix.core.config import AuthConfig


class KeyService:
    def __init__(self, config: AuthConfig) -> None:
        self._key_folder = config.key_folder
        self._private_key = self._read_key(name="private.pem")
        self._public_key = self._read_key(name="public.pem")

    def get_private_key(self) -> str:
        return self._private_key

    def get_public_key(self) -> str:
        return self._public_key

    def _read_key(self, name: str) -> str:
        key_path = self._key_folder.joinpath(name)
        with open(file=key_path, mode="r") as key:
            return key.read()
