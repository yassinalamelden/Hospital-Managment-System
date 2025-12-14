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

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name}"
