import pytest

from authix.domain.password_validation.validators.min_uppercase import MinUppercaseValidator

test_cases = [
    ("a", 1),
    ("aA", 1),
    ("aa", 1),
    ("AaAa", 0),
    ("AA", 0),
]


@pytest.mark.parametrize("password,error_count", test_cases)
def test_min_uppercase_validator(password: str, error_count: int) -> None:
    validator = MinUppercaseValidator(2)
    error_details: list[str] = []
    validator.validate(password=password, error_details=error_details)
    assert len(error_details) == error_count
