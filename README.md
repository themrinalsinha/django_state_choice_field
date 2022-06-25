# dj_enum (alpha)

### Example
```python
from dj_enum import ActionEnum, ChoiceField

# models.py
class PaymentStatus(ActionEnum):
    NOT_STARTED = 'not_started'
    UNDER_PROCESS = 'under_process'
    FAILED = 'failed'
    SUCCESS = 'success'
    CANCELLED = 'cancelled'
    NOT_REQUIRED = 'not_required'

    __states__ = {
        NOT_STARTED: (),
        UNDER_PROCESS: (NOT_STARTED, FAILED),
        FAILED: (UNDER_PROCESS, ),
        SUCCESS: (UNDER_PROCESS, NOT_STARTED),
        CANCELLED: (NOT_STARTED, NOT_REQUIRED, FAILED, SUCCESS),
        NOT_REQUIRED: (NOT_STARTED, ),
    }

class Orders(models.Model):
    payment_status = ChoiceField(PaymentStatus, default=PaymentStatus.NOT_STARTED, max_length=64)
    created_on = models.DateTimeField(auto_now_add=True)
    ended_on = models.DateTimeField(null=True, blank=True)
```

```python
In [1]: from app.models import *

In [2]: order = Order.objects.create()

In [3]: order.payment_status
Out[3]: PaymentStatus.NOT_STARTED # default status

In [4]: order.payment_status = PaymentStatus.UNDER_PROCESS
In [4]: order.save() # will work as it is a valid state change

In [5]: order.payment_status = PaymentStatus.CANCELLED
InvalidStateChangeError: ['under_process -> cancelled is not a valid transition for PaymentStatus']
```
