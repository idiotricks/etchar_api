from django.db import models

from utils.models import Timestamp, generate_string_code


class Employee(Timestamp):
    PREFIX = 'EMP'
    STATUS_MARRIED = 'married'
    STATUS_SINGLE = 'single'
    MARITAL_STATUS_CHOICES = (
        (STATUS_MARRIED, 'Married'),
        (STATUS_SINGLE, 'Single')
    )

    employee_code = models.CharField(max_length=10, unique=True)
    user = models.OneToOneField('auth.User', related_name='useremployee', on_delete=models.CASCADE)
    salary = models.BigIntegerField(default=0)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default=STATUS_SINGLE)
    children = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.employee_code

    def save(self, *args, **kwargs):
        if not self.employee_code:
            self.employee_code = generate_string_code(Employee)

        super(Employee, self).save(*args, **kwargs)
