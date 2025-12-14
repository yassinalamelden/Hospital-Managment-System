from django.db import models
from .person import Person

class Patient(Person):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    medical_history = models.TextField(blank=True, null=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name
