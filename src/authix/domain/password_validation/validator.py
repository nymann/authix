from abc import ABC
from abc import abstractmethod


class Validator(ABC):
    @abstractmethod
    def validate(self, password: str, error_details: list[str]) -> None:
        raise NotImplementedError
