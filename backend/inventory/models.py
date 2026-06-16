from django.db import models

class InventoryItem(models.Model):

    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('LOW_STOCK', 'Low Stock'),
        ('OUT_OF_STOCK', 'Out of Stock'),
    )

    item_name = models.CharField(max_length=200)

    item_code = models.CharField(max_length=100, unique=True)

    quantity = models.IntegerField()

    supplier = models.CharField(max_length=200)

    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)

    linked_apparatus = models.CharField(max_length=200)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name