from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Patient
from billing.models import Bill

class InvoiceViewTests(TestCase):
    def setUp(self):
        # Create a patient directly
        self.patient = Patient.objects.create(
            name="Test Patient",
            age=30,
            gender="Male",
            phone="555-0199"
        )
        self.client = Client()

    def test_print_invoice_hidden_when_pending(self):
        """
        Verify that the print button is not shown when payment status is PENDING.
        """
        bill = Bill.objects.create(
            patient=self.patient,
            payment_status='PENDING',
            total_amount=100.00
        )
        url = reverse('bill-detail', args=[bill.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        # Check that the print button is NOT present
        self.assertNotContains(response, 'onclick="window.print()"')
        # Check that the fallback message IS present
        self.assertContains(response, 'Invoice available after payment')

    def test_print_invoice_visible_when_paid(self):
        """
        Verify that the print button is shown when payment status is PAID.
        """
        bill = Bill.objects.create(
            patient=self.patient,
            payment_status='PAID',
            total_amount=100.00
        )
        url = reverse('bill-detail', args=[bill.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        # Check that the print button IS present
        self.assertContains(response, 'onclick="window.print()"')
