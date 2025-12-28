from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Patient, Doctor
from operations.models import Appointment
from billing.models import Bill
from django.utils import timezone
from datetime import timedelta

class PatientDashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.patient = Patient.objects.create(
            name="John Doe",
            age=30,
            gender="Male",
            phone="1234567890",
            blood_type="O+"
        )
        self.doctor = Doctor.objects.create(
            name="Dr. Smith",
            age=45,
            gender="Male",
            phone="0987654321",
            specialty="General"
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date_time=timezone.now() + timedelta(days=1),
            status="Scheduled"
        )
        self.bill = Bill.objects.create(
            patient=self.patient,
            room_charges=100,
            doctor_fees=50,
            medicine_cost=20,
            payment_status="PENDING"
        )

    def test_dashboard_view(self):
        url = reverse('patient-dashboard', kwargs={'pk': self.patient.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
        self.assertContains(response, "Dr. Smith")
        self.assertContains(response, "170.00") # Total amount (100+50+20)
        
        # Check context
        self.assertIn('patient', response.context)
        self.assertIn('appointments', response.context)
        self.assertIn('bills', response.context)
        
        self.assertEqual(len(response.context['appointments']), 1)
        self.assertEqual(len(response.context['bills']), 1)
