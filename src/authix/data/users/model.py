from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from pydantic import UUID4


class UserModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    email: str
    password_hash: str

    def to_dict(self) -> dict[str, str]:
        return {
            "id": str(self.id),
            "email": self.email,
            "password_hash": self.password_hash,
        }
