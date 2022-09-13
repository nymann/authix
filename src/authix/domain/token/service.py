from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt
from passlib.context import CryptContext

from authix.data.users.model import UserModel
from authix.domain.key.service import KeyService


class TokenService:
    def __init__(self, key_service: KeyService) -> None:
        self._key_service = key_service
        self._pwd_context = CryptContext(schemes=["bcrypt"])

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(secret=plain_password, hash=hashed_password)

    def get_password_hash(self, plain_password: str) -> str:
        return self._pwd_context.hash(secret=plain_password)

    def create_access_token(self, user: UserModel) -> str:
        claims = {
            "id": str(user.id),
            "email": user.email,
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5),
        }
        private_key = self._key_service.get_private_key()
        return jwt.encode(payload=claims, key=private_key, algorithm="RS256")
