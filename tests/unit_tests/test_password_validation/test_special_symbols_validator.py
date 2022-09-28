from authix.domain.password_validation.validators.min_special_symbols import MinSpecialSymbolsValidator


def test_special_symbols_negative() -> None:
    validator = MinSpecialSymbolsValidator("a", 2)
    error_details: list[str] = []
    validator.validate("a", error_details=error_details)
    assert error_details


def test_special_symbols_positive() -> None:
    validator = MinSpecialSymbolsValidator("a", 2)
    error_details: list[str] = []
    validator.validate("aa", error_details=error_details)
    assert not error_details
