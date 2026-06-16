from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin'),
        ('MODULE_ADMIN', 'Module Admin'),
        ('USER', 'User'),
    )

    MODULE_CHOICES = (
        ('APPARATUS', 'Apparatus'),
        ('ENGINEERING', 'Engineering'),
        ('TECHNICAL', 'Technical'),
        ('INVENTORY', 'Inventory'),
        ('FINANCE', 'Finance'),
    )

    name = models.CharField(max_length=100, blank=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

    assigned_module = models.CharField(
        max_length=50,
        choices=MODULE_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username