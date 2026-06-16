from django.db import models

class EngineeringProject(models.Model):

    STATUS_CHOICES = (
        ('PLANNING', 'Planning'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
    )

    project_name = models.CharField(max_length=200)

    project_code = models.CharField(max_length=100, unique=True)

    department = models.CharField(max_length=100)

    project_manager = models.CharField(max_length=100)

    start_date = models.DateField()

    end_date = models.DateField()

    budget = models.DecimalField(max_digits=12, decimal_places=2)

    linked_apparatus = models.CharField(max_length=200)

    linked_inventory_item = models.CharField(max_length=200)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES)

    description = models.TextField()

    def __str__(self):
        return self.project_name