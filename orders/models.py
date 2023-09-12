from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    probation = models.DateTimeField(null=True, blank=True)
    position = models.CharField(max_length=255)


class Order(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    employee = models.ForeignKey(to=Employee, on_delete=models.PROTECT)

    def __str__(self):
        return f"Order:{self.pk} for {self.employee.username}"
