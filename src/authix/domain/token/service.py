from datetime import datetime
from datetime import timedelta
from datetime import timezone

import bcrypt
import jwt

from authix.data.users.model import UserModel
from authix.domain.key.service import KeyService


class TokenService:
    def __init__(self, key_service: KeyService) -> None:
        self._key_service = key_service
        self._encoding = "utf-8"

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self._encoding),
            hashed_password.encode(self._encoding),
        )

    def create_password_hash(self, plain_password: str) -> str:
        hashed_password = bcrypt.hashpw(
            plain_password.encode(self._encoding),
            bcrypt.gensalt(),
        )
        return hashed_password.decode(self._encoding)

    def create_access_token(self, user: UserModel) -> str:
        claims = {
            "id": str(user.id),
            "email": user.email,
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5),
        }
        private_key = self._key_service.get_private_key()
        return jwt.encode(payload=claims, key=private_key, algorithm="RS256")
