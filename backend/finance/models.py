from django.db import models

class FinanceTransaction(models.Model):

    TRANSACTION_TYPES = (
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    department = models.CharField(max_length=100)

    description = models.TextField()

    linked_module = models.CharField(max_length=100)

    transaction_date = models.DateField()

    created_by = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"