from __future__ import annotations

from enum import Enum
from typing import Any, cast

from django.db import models
from django.db.models import Model

from .exceptions import InvalidStateEnumError
from .utils import validate_state_change


class StateEnum(models.TextChoices):
    """
    A state enum that can be used with a ```StateChoiceField``` to provide a state
    machine like functionality.
    """

    __states__: dict = {}
    __default__: StateEnum = None

    @classmethod
    def is_valid_transition(
        cls, from_state: str | StateEnum, to_state: str | StateEnum
    ) -> bool:
        """
        Check if a transition from one state to another is valid.

        Args:
            from_state (str | StateEnum): The current state.
            to_state (str | StateEnum): The state to transition to.

        Returns:
            bool: True if the transition is valid, False otherwise.
        """
        return (
            from_state == to_state
            or not cls.__states__
            or from_state in cls.valid_transition_states(to_state)
        )

    @classmethod
    def valid_transition_states(cls, to_state: str | StateEnum) -> list[str]:
        """
        Get a list of valid states to transition to from the given state.

        Args:
            to_state (str | StateEnum): The state to transition to.

        Returns:
            list[str]: A list of valid states to transition to.
        """
        return cls.__states__.get(to_state, [])

    @classmethod
    def default(cls) -> StateEnum:
        """
        Get the default state.

        Returns:
            StateEnum: The default state.
        """
        if cls.__default__:
            return cast(StateEnum, cls(cls.__default__))
        return None

    @classmethod
    def field(cls, **kwargs) -> StateChoiceField:
        """
        Get a ```StateChoiceField``` instance for this enum.

        Returns:
            StateChoiceField: A ```StateChoiceField``` instance for this enum.
        """
        return StateChoiceField(cls, **kwargs)

    @classmethod
    def get(cls, value, default=None):
        """
        Get the enum member for the given value.

        Args:
            value: The value to get the enum member for.
            default: The default value to return if the enum member is not found.

        Returns:
            The enum member for the given value, or the default value if the enum
            member is not found.
        """
        if isinstance(value, (cls, Enum)):
            return value

        if isinstance(value, str):
            try:
                return cls[value]
            except KeyError:
                pass

        return default


class StateChoiceField(models.CharField):
    """
    A Django model field that can be used to store a state enum.

    :param state_enum: The state enum that this field should use.
    :type state_enum: StateEnum
    """

    def __init__(self, state_enum: StateEnum, *args: Any, **kwargs: Any) -> None:
        if state_enum.default():
            kwargs["default"] = state_enum.default()

        self.state_enum = state_enum
        super().__init__(*args, **kwargs)

    def __checks(self, sender, **kwargs):
        att_name = self.get_attname()
        pvt_name = f"_state__{att_name}"
        state_enum = self.state_enum

        def set_value(self, new_state):
            if new_state is models.NOT_PROVIDED:
                new_state = None

            previous_state = getattr(self, pvt_name, new_state)
            if new_state and not isinstance(new_state, state_enum):
                try:
                    new_state = state_enum(new_state)
                except ValueError:
                    raise InvalidStateEnumError(
                        f"{new_state} is not one of the available choices for "
                        f"{state_enum.__name__}"
                    )

            setattr(self, pvt_name, new_state)
            self.__dict__[att_name] = new_state
            validate_state_change(state_enum, previous_state, new_state)

        def get_value(self):
            return getattr(self, pvt_name)

        def del_value(self):
            self.__dict__[att_name] = None
            return setattr(self, pvt_name, None)

        if not sender._meta.abstract:
            setattr(sender, att_name, property(get_value, set_value, del_value))

    def contribute_to_class(
        self,
        cls: type[Model],
        name: str,
        private_only: bool = False,
        virtual_only=models.NOT_PROVIDED,
    ) -> None:
        super().contribute_to_class(cls, name)
        models.signals.class_prepared.connect(self.__checks, sender=cls)

    def validate(self, value: Any, model_instance: Model) -> None:
        super().validate(value, model_instance)
        validate_state_change(
            self.state_enum, self.value_from_object(model_instance), value
        )

    def deconstruct(self) -> Any:
        *_, kwargs = super().deconstruct()
        kwargs["state_enum"] = self.state_enum

        if "default" in kwargs and isinstance(kwargs["default"], self.state_enum):
            kwargs["default"] = kwargs["default"].value

        return *_, kwargs
