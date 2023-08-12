import bcrypt

from authix.domain.token.password_hashing_strategy import PasswordHashingStrategy


class BcryptPasswordHashingStrategy(PasswordHashingStrategy):
    def __init__(self) -> None:
        self._charset = "utf-8"

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self._charset),
            hashed_password.encode(self._charset),
        )

    def create_password_hash(self, plain_password: str) -> str:
        hashed_password = bcrypt.hashpw(
            plain_password.encode(self._charset),
            bcrypt.gensalt(rounds=10),
        )
        return hashed_password.decode(self._charset)
