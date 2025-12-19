from django.db import models
from .person import Person

class Doctor(Person):
    SPECIALTY_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Pediatrics', 'Pediatrics'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Dermatology', 'Dermatology'),
        ('General', 'General'),
    ]

    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default='50.00')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name}"
