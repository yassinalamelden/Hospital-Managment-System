from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models.patient import Patient

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        # Create a patient profile for non-staff users
        # For simplicity, we use the username as the name initially, 
        # user can update it later.
        Patient.objects.create(user=instance, name=instance.username)

@receiver(post_save, sender=User)
def save_patient_profile(sender, instance, **kwargs):
    if not instance.is_staff and hasattr(instance, 'patient'):
        instance.patient.save()
