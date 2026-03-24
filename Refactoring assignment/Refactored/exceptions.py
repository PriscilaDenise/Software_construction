class BankingError(Exception):
    """Base exception for banking system."""
    pass


class AuthenticationError(BankingError):
    """Raised when login credentials are invalid."""
    pass


class InsufficientFundsError(BankingError):
    """Raised when withdrawal amount exceeds account balance."""
    pass


class InvalidAmountError(BankingError):
    """Raised when an amount entered is invalid."""
    pass


class DataStorageError(BankingError):
    """Raised when data loading or saving fails."""
    pass