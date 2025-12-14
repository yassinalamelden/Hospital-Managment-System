from django.db import models

class Bill(models.Model):
    patient = models.ForeignKey(
        'accounts.Patient', 
        on_delete=models.CASCADE, 
        related_name='bills'
    )
    issued_date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    
    room_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    doctor_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    medicine_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Auto-calculate total
        self.total_amount = self.room_charges + self.doctor_fees + self.medicine_cost
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Paid" if self.is_paid else "Unpaid"
        return f"Bill for {self.patient} - {self.total_amount} ({status})"
