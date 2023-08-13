from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jwt.jwt import JWT
from jwt.utils import get_int_from_datetime

from authix.data.users.model import UserModel
from authix.domain.key.service import KeyService
from authix.domain.token.password_hashing_strategies.argon_id import ArgonIDPasswordHashingStrategy
from authix.domain.token.password_hashing_strategy import PasswordHashingStrategy


class TokenService:
    def __init__(self, key_service: KeyService) -> None:
        self._key_service = key_service
        self._charset = "utf-8"
        self._password_hasher: PasswordHashingStrategy = ArgonIDPasswordHashingStrategy()
        self.json_web_token = JWT()  # type: ignore
        self.private_key = self._key_service.get_private_key()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._password_hasher.verify_password(plain_password=plain_password, hashed_password=hashed_password)

    def create_password_hash(self, plain_password: str) -> str:
        return self._password_hasher.create_password_hash(plain_password)

    def create_access_token(self, user: UserModel) -> str:
        utc_now = datetime.now(tz=timezone.utc)
        claims = {
            "id": str(user.id),
            "email": user.email,
            "iat": get_int_from_datetime(utc_now),
            "exp": get_int_from_datetime(utc_now + timedelta(minutes=5)),
        }
        return self.json_web_token.encode(payload=claims, key=self.private_key, alg="RS256")
