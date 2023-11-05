# django_state_choice_field
[![Checks & Tests](https://github.com/themrinalsinha/django_state_choice_field/actions/workflows/checks_and_tests.yaml/badge.svg)](https://github.com/themrinalsinha/django_state_choice_field/actions/workflows/checks_and_tests.yaml)

It includes a `StateChoiceField` that comes with reusable `TextChoices` and validation for state changes. This feature enhances flexibility and data integrity.

## Requirements
- Python 3.6+
- Django 2.2+

## Installation
To set up `django_state_choice_field`, you can easily install it with pip.
```shell
$ pip install django_state_choice_field
```

## Example
Consider a scenario where we have a model called `Order` that includes the storage of the order's payment status. This payment status can fall into one of the following in `PaymentStatus`.

It also defines the state transitions that are allowed for each state. For example, a payment status of `IN_PROGRESS` can only be changed to `FAILED` or `COMPLETED`. This is done by defining the `__states__` attribute in the `PaymentStatus` class which extends `StateEnum`.
```python
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
```
Model `Order` can be defined as follows. The `payment_status` field is defined as a `StateChoiceField` with the `PaymentStatus` enum class.
```python
from django.db import models

class Orders(models.Model):
    product_name = models.CharField(max_length=100)
    payment_status = StateChoiceField(
        PaymentStatus, default=PaymentStatus.NOT_STARTED, max_length=20
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Usage**
```shell
>>> order = Order.objects.create(product_name="Product 1")
>>> order.payment_status
<PaymentStatus.NOT_STARTED: 'not_started'>

>>> order.payment_status = PaymentStatus.IN_PROGRESS
>>> order.save()

>>> order.payment_status
<PaymentStatus.IN_PROGRESS: 'in_progress'>

# Now, if we try to change the payment status to CANCELLED, it will raise a InvalidTransitionError error.
>>> order.payment_status = PaymentStatus.CANCELLED

django_state_choice_field.exceptions.InvalidTransitionError: [in_progress -> cancelled is not a valid transition for PaymentStatus']
```
