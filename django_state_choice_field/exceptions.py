from django.core.exceptions import ValidationError


class InvalidStateEnumError(ValidationError):
    """
    Raised when a state enum is not properly configured.
    """


class InvalidTransitionError(ValidationError):
    """
    Raised when a transition is not valid.
    """
