import argon2

from authix.domain.token.password_hashing_strategy import PasswordHashingStrategy


class ArgonIDPasswordHashingStrategy(PasswordHashingStrategy):
    def __init__(self) -> None:
        self._password_hasher = argon2.PasswordHasher(
            encoding="utf-8",
            hash_len=32,
            memory_cost=7168,
            parallelism=1,
            salt_len=16,
            time_cost=5,
            type=argon2.Type.ID,
        )

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return self._password_hasher.verify(hash=hashed_password, password=plain_password)
        except argon2.exceptions.VerificationError:
            return False

    def create_password_hash(self, plain_password: str) -> str:
        return self._password_hasher.hash(plain_password)
