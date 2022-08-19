from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext
from pydantic.types import SecretStr

from auth_service.data.users.model import UserModel


class TokenService:
    def __init__(self, secret: SecretStr) -> None:
        self._secret = secret.get_secret_value()
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
        return jwt.encode(claims=claims, key=self._secret, algorithm="HS256")

    def decode(self, access_token: str) -> dict[str, Any]:
        return jwt.decode(token=access_token, key=self._secret, algorithms=["HS256"])
