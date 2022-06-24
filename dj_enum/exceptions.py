from django.core.exceptions import ValidationError


class InvalidEnumValue(ValidationError):
    pass

class InvalidStateChangeError(ValidationError):
    pass
