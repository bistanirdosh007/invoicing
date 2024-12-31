# invoicing/models.py
from django.db import models

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer_name}"
