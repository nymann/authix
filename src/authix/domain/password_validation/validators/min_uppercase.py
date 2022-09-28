from authix.domain.password_validation.validator import Validator


class MinUppercaseValidator(Validator):
    def __init__(self, minimum_count: int) -> None:
        self.minimum_count = minimum_count
        self.error_text = f"Atleast {self.minimum_count} uppercase characters."

    def validate(self, password: str, error_details: list[str]) -> None:
        uppercase_count = sum(character.isupper() for character in password)
        if uppercase_count < self.minimum_count:
            error_details.append(self.error_text)
