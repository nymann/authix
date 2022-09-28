import pytest

from authix.domain.password_validation.validators.max_length import MaxLengthValidator

test_cases = [
    ("a", 0),
    ("aa", 0),
    ("aaa", 1),
]


@pytest.mark.parametrize("password,error_count", test_cases)
def test_max_length_validator(password: str, error_count: int) -> None:
    validator = MaxLengthValidator(2)
    error_details: list[str] = []
    validator.validate(password=password, error_details=error_details)
    assert len(error_details) == error_count
