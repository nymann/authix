import pytest

from authix.domain.password_validation.validators.min_length import MinLengthValidator

test_cases = [
    ("a", 1),
    ("aa", 0),
    ("aaa", 0),
]


@pytest.mark.parametrize("password,error_count", test_cases)
def test_min_length_validator(password: str, error_count: int) -> None:
    validator = MinLengthValidator(2)
    error_details: list[str] = []
    validator.validate(password=password, error_details=error_details)
    assert len(error_details) == error_count
