from django.db import models

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
    room_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    doctor_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    medicine_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Auto-calculate total from items if saved instance (to access ManyToMany/Reverse FK)
        if self.pk:
            items_total = sum(item.total_price for item in self.items.all())
            # If we have items, use their total. logic: if items exist, they override the flat fields sum.
            # OR we can just say total_amount is always sum of items + flat fields?
            # Let's say: Total Amount = Sum of Items.
            # But we need to handle the case where flat fields are used manually.
            # For this feature, we want auto-generated items. 
            # Let's make total_amount = sum(items.total_price).
            # But wait, self.items.all() won't be populated on first save if we haven't added items yet.
            if items_total > 0:
                 self.total_amount = items_total
            else:
                 self.total_amount = self.room_charges + self.doctor_fees + self.medicine_cost
        else:
             self.total_amount = self.room_charges + self.doctor_fees + self.medicine_cost
        
        # Update is_paid based on status
        if self.payment_status == 'PAID':
            self.is_paid = True
        elif self.payment_status == 'PENDING':
             self.is_paid = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill for {self.patient} - {self.total_amount} ({self.payment_status})"
