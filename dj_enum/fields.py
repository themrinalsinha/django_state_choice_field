from typing import cast
from enum import Enum
from django.db import models
from .exceptions import InvalidEnumValue
from .utils import validate_state_change


class ActionEnum(models.TextChoices):
    __states__ = {}
    __default__ = None

    @classmethod
    def is_valid_transition(cls, from_state, to_state):

        if isinstance(from_state, cls):
            from_state = from_state.value

        if isinstance(to_state, cls):
            to_state = to_state.value

        return (
            from_state == to_state
            or not cls.__states__
            or not (from_state in cls.transition_origins(to_state))
        )

    @classmethod
    def transition_origins(cls, to_state):

        if isinstance(to_state, cls):
            to_state = to_state.value

        return cls.__states__.get(to_state, [])

    @classmethod
    def default(cls):
        if cls.__default__:
            return cast(ActionEnum, cls(cls.__default__))
        return None

    @classmethod
    def field(cls, **kwargs):
        return ChoiceField(cls, **kwargs)

    @classmethod
    def get(cls, value, default=None):
        if isinstance(value, (cls, Enum)):
            return value

        if isinstance(value, str):

            try:
                return cls[value]
            except KeyError:
                ...

        return default

class ChoiceField(models.CharField):
    def __init__(self, action_enum, *args, **kwargs):
        if action_enum.default():
            kwargs["default"] = action_enum.default()

        self.action_enum = action_enum
        super().__init__(*args, **kwargs)

    def _checks(self, sender, **kwargs):
        att_name = self.get_attname()
        pvt_att_name = f"_action__{att_name}"
        action_enum = self.action_enum

        def set_value(self, new_state):
            if new_state is models.NOT_PROVIDED:
                new_state = None

            if hasattr(self, pvt_att_name):
                old_state = getattr(self, pvt_att_name)
            else:
                old_state = new_state

            if new_state and not isinstance(new_state, action_enum):
                try:
                    new_state = action_enum(new_state)
                except ValueError:
                    raise InvalidEnumValue(
                        f"{new_state} is not one of the available choices for {action_enum.__name__}"
                    )

            setattr(self, pvt_att_name, new_state)
            self.__dict__[att_name] = new_state
            validate_state_change(action_enum, old_state, new_state)

        def get_value(self):
            return getattr(self, pvt_att_name)

        def del_value(self):
            self.__dict__[att_name] = None
            return setattr(self, pvt_att_name, None)

        if not sender._meta.abstract:
            setattr(sender, att_name, property(get_value, set_value, del_value))

    def contribute_to_class(
        self, cls, name, private_only=False, virtual_only=models.NOT_PROVIDED
    ):
        super().contribute_to_class(cls, name)
        models.signals.class_prepared.connect(self._checks, sender=cls)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        validate_state_change(
            self.action_enum, self.value_from_object(model_instance), value
        )

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        if "default" in kwargs and isinstance(kwargs["default"], self.action_enum):
            kwargs["default"] = kwargs["default"].value

        return name, path, args, kwargs
