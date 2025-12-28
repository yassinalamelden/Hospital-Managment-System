import os
import django
from django.utils import timezone
from datetime import timedelta

# Setup Django if run as standalone, but we will run via shell
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django.setup()

from accounts.models.doctor import Doctor
from accounts.models.patient import Patient
from operations.models.appointment import Appointment
from operations.models.room import Room
from billing.models.bill import Bill
from billing.models.bill_item import BillItem

def verify():
    print("Starting Verification...")

    # 1. Create Data
    doctor = Doctor.objects.create(name="Test Dr", specialty="General", consultation_fee=100.00, age=30, gender="M")
    patient = Patient.objects.create(name="Test Patient", age=25, gender="M", blood_type="O+")
    print(f"Created Doctor: {doctor}, Fee: {doctor.consultation_fee}")
    print(f"Created Patient: {patient}")

    # 2. Test Consultation Billing
    print("\n--- Testing Consultation Billing ---")
    appt = Appointment.objects.create(
        doctor=doctor,
        patient=patient,
        date_time=timezone.now(),
        status='Scheduled'
    )
    print("Appointment Scheduled.")
    
    # Complete Appointment
    appt.status = 'Completed'
    appt.save()
    print("Appointment Completed.")

    # Check Bill
    bill = Bill.objects.filter(patient=patient, payment_status='PENDING').last()
    if bill:
        print(f"Found Bill: {bill}")
        items = bill.items.all()
        print(f"Bill Items: {[str(i) for i in items]}")
        assert items.count() >= 1, "Should have at least 1 item"
        consult_item = items.filter(item_name__contains="Consultation").first()
        if consult_item:
            print(f"Verified Item: {consult_item.item_name} - {consult_item.total_price}")
            assert consult_item.unit_price == 100.00
        else:
            print("ERROR: Consultation item not found!")
    else:
        print("ERROR: Bill not created!")

    # 3. Test Room Billing
    print("\n--- Testing Bed Stay Billing ---")
    room = Room.objects.create(room_number="101-TEST", room_type="General", price_per_night=50.00)
    
    # Admit
    # Manually set admission date in the past
    past_date = timezone.now().date() - timedelta(days=3)
    room.current_patient = patient
    room.admission_date = past_date
    room.save()
    print(f"Patient admitted to Room {room.room_number} on {past_date}")

    # Discharge (Set patient to None)
    room.current_patient = None
    room.save()
    print("Patient discharged.")

    # Check Bill (Should be same bill or new if pending)
    # Re-fetch bill
    bill.refresh_from_db()
    items = bill.items.all()
    print(f"Bill Items Now: {[str(i) for i in items]}")
    
    room_item = items.filter(item_name__contains="Room Charge").first()
    if room_item:
        print(f"Verified Room Item: {room_item.item_name} -> Qty: {room_item.quantity}, Total: {room_item.total_price}")
        # Expected: 3 days * 50 = 150
        # Wait, simple logic in signals: today - admission_date
        # If I run this immediately, today is same as created? no I mocked past_date.
        # Signal uses timezone.now().date().
        # So it should be ~3 days.
        assert room_item.quantity == 3
        assert room_item.total_price == 150.00
    else:
        print("ERROR: Room Charge item not found!")

    # Cleanup
    # doctor.delete()
    # patient.delete()
    # room.delete()
    # bill.delete()
    print("\nVerification Complete.")

if __name__ == "__main__":
    verify()
