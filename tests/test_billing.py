import os
import sys

# === Make sure project root is on sys.path ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.modules.billing import Invoice

if __name__ == "__main__":
    # Create an invoice for a patient
    invoice = Invoice(invoice_id = 1, patient_name = "Amr Mohsen")

    # Add some services/products
    invoice.add_item("Doctor Consultation", 1, 300)
    invoice.add_item("Blood Test", 2, 150)   # 2 tests * 150 = 300
    invoice.add_item("X-Ray", 1, 250)

    # Print the invoice
    invoice.generate_bill()
    invoice.save_to_file("invoice_1.txt")

    # Create an invoice 2 for a patient with 80% insurance coverage
    invoice2 = Invoice(invoice_id = 2, patient_name = "Yassin Mahmoud", insurance_company = "Life Health Care", coverage_percent = 80)

    # Add a service or product
    invoice2.add_item("MRI Scan", 1, 2000)

    # Print the invoice
    invoice2.generate_bill()
    invoice2.save_to_file("invoice_2.text")
    