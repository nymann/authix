from pydantic import BaseModel
from pydantic import UUID4


class UserModel(BaseModel):
    id: UUID4
    email: str
    password_hash: str
