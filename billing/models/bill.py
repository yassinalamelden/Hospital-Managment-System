from django.db import models
from decimal import Decimal

class Bill(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PARTIAL', 'Partial'),
        ('PAID', 'Paid'),
    ]

    patient = models.ForeignKey(
        'accounts.Patient', 
        on_delete=models.CASCADE, 
        related_name='bills'
    )
    issued_date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)  # Deprecated in favor of payment_status? Let's keep for simple boolean check
    
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='CASH')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    # Kept for backward compatibility, but ideally derived from items
    room_charges = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    doctor_fees = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    medicine_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        # Calculate total as sum of items + flat fields
        items_total = Decimal('0.00')
        if self.pk:
            items_total = sum(item.total_price for item in self.items.all())
        
        self.total_amount = self.room_charges + self.doctor_fees + self.medicine_cost + items_total
        
        # Update is_paid based on status
        if self.payment_status == 'PAID':
            self.is_paid = True
        elif self.payment_status == 'PENDING':
             self.is_paid = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill for {self.patient} - {self.total_amount} ({self.payment_status})"
