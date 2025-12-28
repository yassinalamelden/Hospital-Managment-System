from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models.appointment import Appointment
from .models.room import Room
from billing.models.bill import Bill
from billing.models.bill_item import BillItem
import datetime

@receiver(post_save, sender=Appointment)
def create_consultation_bill(sender, instance, created, **kwargs):
    if instance.status == 'Completed':
        # Check if we already billed for this appointment?
        # We can avoid duplicates by checking if a BillItem exists with this name for this bill?
        # Or just trust the signal only fires once for 'Completed'?
        # Ideally we should flag the appointment as 'Billed' but we don't have that field.
        # We'll allow duplicates if status toggles, or we could check if a BillItem exists recently.
        # For this MVP, let's just create the item.
        
        patient = instance.patient
        doctor = instance.doctor
        
        # Find the latest pending bill or create a new one
        bill = Bill.objects.filter(
            patient=patient,
            payment_status='PENDING'
        ).order_by('-id').first()

        if not bill:
            bill = Bill.objects.create(
                patient=patient,
                payment_status='PENDING',
                payment_method='CASH'
            )
        
        item_name = f"Consultation with {doctor}"
        price = doctor.consultation_fee
        
        # Avoid duplicate item for same appointment if run multiple times?
        # A simple check:
        if not BillItem.objects.filter(bill=bill, item_name=item_name, unit_price=price).exists():
            BillItem.objects.create(
                bill=bill,
                item_name=item_name,
                quantity=1,
                unit_price=price
            )

@receiver(pre_save, sender=Room)
def charge_room_on_discharge(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Room.objects.get(pk=instance.pk)
        except Room.DoesNotExist:
            return # New room creation

        # Check for discharge: Old had patient, New has None
        if old_instance.current_patient and not instance.current_patient:
            patient = old_instance.current_patient
            admission_date = old_instance.admission_date
            
            if admission_date:
                today = timezone.now().date()
                # If admission_date is DateField, it's fine. If DateTimeField, convert.
                if isinstance(admission_date, datetime.datetime):
                    admission_date = admission_date.date()
                
                delta = today - admission_date
                days = delta.days
                if days < 1:
                    days = 1 # Minimum 1 day charge
                
                # Find latest pending bill or create
                bill = Bill.objects.filter(
                    patient=patient,
                    payment_status='PENDING'
                ).order_by('-id').first()
                
                if not bill:
                    bill = Bill.objects.create(
                        patient=patient,
                        payment_status='PENDING',
                        payment_method='CASH'
                    )
                
                item_name = f"Room Charge: {old_instance.room_number} ({old_instance.room_type})"
                price_per_day = old_instance.price_per_night
                
                BillItem.objects.create(
                    bill=bill,
                    item_name=item_name,
                    quantity=days,
                    unit_price=price_per_day
                )
                
                # Reset admission date on the instance is handled by the View usually? 
                # Or we should ensure it's cleared so it doesn't persist?
                # The instance.current_patient is None, but instance.admission_date might remain?
                # Let's clear admission_date on the instance
                instance.admission_date = None
