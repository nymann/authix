from authix.domain.password_validation.validator import Validator


class MaxLengthValidator(Validator):
    def __init__(self, maximum_length: int) -> None:
        self.maximum_length = maximum_length

    def validate(self, password: str, error_details: list[str]) -> None:
        if len(password) > self.maximum_length:
            error_details.append(f"Maximum {self.maximum_length} characters.")
