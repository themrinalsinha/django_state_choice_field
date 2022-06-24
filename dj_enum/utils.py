from .exceptions import InvalidStateChangeError, InvalidEnumValue


def _valid_choices(enum, to_value):
    if to_value is None:
        return True

    try:
        enum(to_value)
    except ValueError:
        raise InvalidEnumValue(
            f"{to_value} is not one of the available choices for {enum.__name__}"
        )

def validate_state_change(enum, from_state, to_state):
    _valid_choices(enum, to_state)

    if not enum.is_valid_transition(from_state, to_state):
        raise InvalidStateChangeError(
            f"{from_state} -> {to_state} is not a valid transition for {enum.__name__}"
        )
