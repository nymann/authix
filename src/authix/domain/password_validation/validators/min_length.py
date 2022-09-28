from authix.domain.password_validation.validator import Validator


class MinLengthValidator(Validator):
    def __init__(self, minimum_length: int) -> None:
        self.minimum_length = minimum_length

    def validate(self, password: str, error_details: list[str]) -> None:
        if len(password) < self.minimum_length:
            error_details.append(f"Minimum {self.minimum_length} characters.")
