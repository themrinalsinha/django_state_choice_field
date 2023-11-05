from django.db import models

from django_state_choice_field import StateChoiceField, StateEnum


class PaymentStatus(StateEnum):
    NOT_STARTED = "not_started", "Not Started"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"
    NOT_REQUIRED = "not_required", "Not Required"

    __states__ = {
        NOT_STARTED: (),
        IN_PROGRESS: (NOT_STARTED, FAILED),
        FAILED: (IN_PROGRESS,),
        COMPLETED: (IN_PROGRESS, NOT_REQUIRED),
        NOT_REQUIRED: (IN_PROGRESS,),
        CANCELLED: (NOT_STARTED, NOT_REQUIRED, FAILED, COMPLETED),
    }


class Orders(models.Model):
    product_name = models.CharField(max_length=100)
    status = StateChoiceField(
        PaymentStatus, default=PaymentStatus.NOT_STARTED, max_length=20
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
