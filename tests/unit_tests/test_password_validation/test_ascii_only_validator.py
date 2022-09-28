import pytest

from authix.domain.password_validation.validators.ascii_only import AsciiOnlyValidator

test_cases = [
    ("a", 0),
    ("1", 0),
    ("¹", 1),
    ("ó", 1),
    ("å", 1),
]


@pytest.mark.parametrize("password,error_count", test_cases)
def test_ascii_only_validator(password: str, error_count: int) -> None:
    validator = AsciiOnlyValidator()
    error_details: list[str] = []
    validator.validate(password=password, error_details=error_details)
    assert len(error_details) == error_count
