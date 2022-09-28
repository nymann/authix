from authix.domain.password_validation.validator import Validator


class MinDigitsValidator(Validator):
    def __init__(self, minimum_digits: int) -> None:
        self.min_digits = minimum_digits

    def validate(self, password: str, error_details: list[str]) -> None:
        digit_count = sum(characters.isdigit() for characters in password)
        if digit_count < self.min_digits:
            error_details.append(f"Atleast {self.min_digits} digits")
