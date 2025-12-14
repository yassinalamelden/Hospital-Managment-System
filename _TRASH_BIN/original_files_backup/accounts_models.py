from django.db import models

class Person(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

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
    doctor_id = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name}"

class Patient(Person):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    patient_id = models.CharField(max_length=20, unique=True)
    medical_history = models.TextField(blank=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name
