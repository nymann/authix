from http import HTTPStatus

from fastapi import HTTPException

from authix.core.config import PasswordConfig
from authix.domain.password_validation.validator import Validator
from authix.domain.password_validation.validators.ascii_only import AsciiOnlyValidator
from authix.domain.password_validation.validators.max_length import MaxLengthValidator
from authix.domain.password_validation.validators.min_digits import MinDigitsValidator
from authix.domain.password_validation.validators.min_length import MinLengthValidator
from authix.domain.password_validation.validators.min_lowercase import MinLowercaseValidator
from authix.domain.password_validation.validators.min_special_symbols import MinSpecialSymbolsValidator
from authix.domain.password_validation.validators.min_uppercase import MinUppercaseValidator


class InvalidPasswordError(HTTPException):
    def __init__(self, violations: list[str]) -> None:
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=violations, headers=None)


class PasswordValidator:
    def __init__(self, password_config: PasswordConfig) -> None:
        self.validators: list[Validator] = [
            MinLengthValidator(minimum_length=password_config.min_length),
            MaxLengthValidator(maximum_length=password_config.max_length),
            MinSpecialSymbolsValidator(
                symbols=password_config.symbols,
                minimum_count=password_config.min_special_chars,
            ),
            MinDigitsValidator(minimum_digits=password_config.min_digits),
            MinUppercaseValidator(minimum_count=password_config.min_uppercase_chars),
            MinLowercaseValidator(minimum_count=password_config.min_lowercase_chars),
            AsciiOnlyValidator(),
        ]

    def validate(self, password: str) -> None:
        violations: list[str] = []
        for validator in self.validators:
            validator.validate(password=password, error_details=violations)

        if violations:
            raise InvalidPasswordError(violations=violations)
