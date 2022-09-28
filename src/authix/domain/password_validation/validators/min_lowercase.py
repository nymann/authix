from authix.domain.password_validation.validator import Validator


class MinLowercaseValidator(Validator):
    def __init__(self, minimum_count: int) -> None:
        self.minimum_count = minimum_count
        self.error_text = f"Atleast {self.minimum_count} lowercase characters."

    def validate(self, password: str, error_details: list[str]) -> None:
        lowercase_count = sum(character.islower() for character in password)
        if lowercase_count < self.minimum_count:
            error_details.append(self.error_text)
