from authix.domain.password_validation.validator import Validator


class MinSpecialSymbolsValidator(Validator):
    def __init__(self, symbols: str, minimum_count: int) -> None:
        self.symbols = symbols
        self.minimum_count = minimum_count
        if self.minimum_count > 1:
            self.error_text = f"Minimum {self.minimum_count} symbols ('{self.symbols}')"
        else:
            self.error_text = f"Minimum {self.minimum_count} symbol ('{self.symbols}')"

    def validate(self, password: str, error_details: list[str]) -> None:
        symbol_count = sum(character in self.symbols for character in password)
        if symbol_count >= self.minimum_count:
            return
        error_details.append(self.error_text)
