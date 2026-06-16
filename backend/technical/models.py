from django.db import models

class Document(models.Model):

    MODULE_CHOICES = (
        ('APPARATUS', 'Apparatus'),
        ('ENGINEERING', 'Engineering'),
        ('TECHNICAL', 'Technical'),
        ('INVENTORY', 'Inventory'),
        ('FINANCE', 'Finance'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    module = models.CharField(max_length=50, choices=MODULE_CHOICES)

    uploaded_by = models.CharField(max_length=100)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    file = models.FileField(upload_to='documents/')

    version = models.IntegerField(default=1)

    def __str__(self):
        return self.title
class TechnicalReport(models.Model):

    REPORT_TYPES = (
        ('TESTING', 'Testing'),
        ('MAINTENANCE', 'Maintenance'),
        ('INSPECTION', 'Inspection'),
        ('SOP', 'SOP'),
    )

    report_title = models.CharField(max_length=200)

    report_type = models.CharField(
        max_length=50,
        choices=REPORT_TYPES
    )

    linked_project = models.CharField(max_length=200)

    linked_apparatus = models.CharField(max_length=200)

    created_by = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    remarks = models.TextField()

    file = models.FileField(upload_to='technical_reports/')

    def __str__(self):
        return self.report_title