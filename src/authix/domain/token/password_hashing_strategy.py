from abc import ABC
from abc import abstractmethod


class PasswordHashingStrategy(ABC):
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create_password_hash(self, plain_password: str) -> str:
        raise NotImplementedError
