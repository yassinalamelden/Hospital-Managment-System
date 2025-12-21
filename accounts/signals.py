from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models.patient import Patient

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    if created:
        Patient.objects.create(
            user=instance,
            name=instance.username,
            age=0,  
            address="Please update address", 
            phone="0000000000", 
            blood_type="O+", 
            medical_history="None"
        )

@receiver(post_save, sender=User)
def save_patient_profile(sender, instance, **kwargs):
    if hasattr(instance, 'patient'):
        instance.patient.save()
