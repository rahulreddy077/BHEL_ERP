from django.db import models

class Apparatus(models.Model):

    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('UNDER_MAINTENANCE', 'Under Maintenance'),
        ('INACTIVE', 'Inactive'),
    )

    name = models.CharField(max_length=200)

    serial_number = models.CharField(max_length=100, unique=True)

    department = models.CharField(max_length=100)

    installation_date = models.DateField()

    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES)

    linked_engineering_project = models.CharField(max_length=200)

    def __str__(self):
        return self.name