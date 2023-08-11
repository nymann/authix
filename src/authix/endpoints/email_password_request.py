from pydantic import BaseModel
from pydantic import SecretStr


class EmailPasswordRequest(BaseModel):
    email: str
    password: SecretStr
