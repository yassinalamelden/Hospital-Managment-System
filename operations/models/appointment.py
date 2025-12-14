from django.db import models

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    doctor = models.ForeignKey(
        'accounts.Doctor', 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    patient = models.ForeignKey(
        'accounts.Patient', 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

    def __str__(self):
        return f"Appointment: {self.patient} with {self.doctor} on {self.date_time}"
