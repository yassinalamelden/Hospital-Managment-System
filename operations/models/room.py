from django.db import models

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('ICU', 'ICU'),
        ('General', 'General'),
        ('Private', 'Private'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    current_patient = models.OneToOneField(
        'accounts.Patient', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='room'
    )
    admission_date = models.DateField(null=True, blank=True)

    @property
    def is_occupied(self):
        return self.current_patient is not None

    def __str__(self):
        status = "Occupied" if self.is_occupied else "Available"
        return f"Room {self.room_number} ({self.room_type}) - {status}"
