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
    # Using string reference to avoid import issues
    current_patient = models.OneToOneField(
        'accounts.Patient', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='room'
    )

    @property
    def is_occupied(self):
        return self.current_patient is not None

    def __str__(self):
        status = "Occupied" if self.is_occupied else "Available"
        return f"Room {self.room_number} ({self.room_type}) - {status}"

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
