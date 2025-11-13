class DomainException(Exception):
    """
    Base exception class for application-specific business rule failures.
    These exceptions typically map to a 400-level HTTP error response.
    """
    pass

class IntegrityConflictException(DomainException):
    """Exception raised when a unique constraint or integrity check fails."""
    pass