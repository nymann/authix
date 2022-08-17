from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any, Optional
from uuid import uuid4

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from pydantic import UUID4

auth_router = APIRouter(tags=["Authentication"])


class UserModel(BaseModel):
    id: UUID4
    email: str
    password_hash: str


pwd_context = CryptContext(schemes=["bcrypt"])
secret: str = "Super secret, yes."


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(secret=plain_password)


knj = UserModel(id=uuid4(), email="kristian@nymann.dev", password_hash=get_password_hash(plain_password="test123"))

user_db: dict[UUID4, UserModel] = {knj.id: knj}
refresh_tokens: dict[str, UUID4] = {}
revoked: dict[str, datetime] = {}


def find_user(email: str) -> Optional[UserModel]:
    for user in user_db.values():
        if user.email == email:
            return user


class AuthResponse(BaseModel):
    jwt: str
    refresh_token: str


def create_access_token(user: UserModel) -> str:
    claims = {
        "id": str(user.id),
        "email": user.email,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims=claims, key=secret, algorithm="HS256")


@auth_router.post("/login")
async def login(email: str, password: str) -> AuthResponse:
    """Authenticates a user by creating a new refresh token, that can be used to create new JWTs."""
    user = find_user(email=email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not verify_password(plain_password=password, hashed_password=user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    refresh_token = str(uuid4())
    refresh_tokens[refresh_token] = user.id
    return AuthResponse(
        jwt=create_access_token(user=user),
        refresh_token=refresh_token,
    )


@auth_router.delete("/logout")
async def logout(refresh_token: str) -> None:
    """Logs a user out by deleting their refresh token, and broadcasting a revoke event."""
    user_id = refresh_tokens.pop(refresh_token)
    if user_id is None:
        return
    revoked[str(user_id)] = datetime.now(tz=timezone.utc) + timedelta(minutes=5)


@auth_router.post("/jwt")
async def create_jwt(refresh_token: str) -> str:
    """Create a new JWT from a refresh token."""
    user_id = refresh_tokens[refresh_token]
    user = user_db[user_id]
    return create_access_token(user=user)


@auth_router.get("/test")
async def test_access_token(access_token: str) -> dict:
    encoded_data: dict[str, Any] = jwt.decode(token=access_token, key=secret, algorithms=["HS256"])
    user_id: str = encoded_data["id"]
    try:
        revoked_dt = revoked[user_id]
    except KeyError:
        return encoded_data
    exp: datetime = datetime.fromtimestamp(encoded_data["exp"], tz=timezone.utc)
    if exp < revoked_dt:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Revoked token")
    return encoded_data
