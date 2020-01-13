from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.models import Timestamp, generate_string_code, generate_user


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
    first_name = models.CharField(max_length=100, default='John')
    last_name = models.CharField(max_length=100, default='Doe')
    email = models.EmailField(max_length=100, default='johndoe@mail.com')
    salary = models.BigIntegerField(default=0)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default=STATUS_SINGLE)
    children = models.PositiveIntegerField(default=0)
    is_publish = models.BooleanField(default=False)

    def __str__(self):
        return self.employee_code


@receiver(post_save, sender=Employee)
def create_employee(sender, instance=None, created=False, **kwargs):
    if instance.user:
        user = User.objects.get(username=instance.user.username)
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.email = instance.email
        user.is_active = instance.is_publish
        user.save()
