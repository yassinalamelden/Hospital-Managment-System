import os


class InvoiceItem:
    '''
    InvoiceItem class is used to represent one service or product in the bill
    For Example: X-Ray, quantity 1, price 300
    '''

    def __init__(self, description, quantity, price):
        self.description = description
        self.quantity = quantity
        self.price = price

    # Return Price of this item
    def get_subtotal(self):
        return self.quantity * self.price
    

class Invoice:

    def __init__(self, invoice_id, patient_name, insurance_company = None, coverage_percent = 0):
        self.invoice_id = invoice_id
        self.patient_name = patient_name
        self.items = []

        """
        insurance_company: name of the insurance (e.g. 'Life Health Care') or None
        coverage_percent: how much insurance covers from total (0-100), 0 means no coverage
        """
        self.insurance_company = insurance_company
        self.coverage_percent = coverage_percent

    # Set or Update the insurance info for this invoice
    def set_insurance(self, insurance_company, coverage_percent):
        self.insurance_company = insurance_company
        self.coverage_percent = coverage_percent

    # How much the insurance will pay
    def get_insurance_covered_amount(self):
        if not self.insurance_company or self.coverage_percent <= 0:
            return 0
        return self.get_total() * (self.coverage_percent / 100.0)

    # How much the patient must pay after insurance
    def get_patient_payable(self):
        return self.get_total() - self.get_insurance_covered_amount()

    # Add new item
    def add_item(self, description, quantity, price):
        item = InvoiceItem(description, quantity, price)
        self.items.append(item)

    # get the total of the bill
    def get_total(self):
        total = 0
        for item in self.items:
            total += item.get_subtotal()
        return total
    
    # Generating the bill for the patient
    def generate_bill(self):
        print(f"---------BILL-------")
        print(f"Patient ID : {self.invoice_id}")
        print(f"Patient: {self.patient_name}")

        if self.insurance_company:
            print(f"Insurance: {self.insurance_company}")
            print(f"Coverage: {self.coverage_percent}")
        else:
            print("Insurance: None")

        print("Items: ")
        for item in self.items:
            print(f" - {item.description} x{item.quantity} = {item.get_subtotal()}")

        total = self.get_total()
        insurance_part = self.get_insurance_covered_amount()
        patient_part = self.get_patient_payable()

        print(f"Total bill: {self.get_total()}")
        if self.insurance_company:
            print(f"Covered by insurance: {insurance_part}")
            print(f"Patient must pay: {patient_part}")
        print("----------------------")

    # Saving the bill in a seperate file in .txt to print it for the user
    def save_to_file(self, filename):
        """
        Saves the bill to a text file.
        """
        # Create folder if it doesn't exist
        os.makedirs("invoices", exist_ok=True)

        # File path
        filename = f"invoices/invoice_{self.invoice_id}.txt"
        
        with open(filename, "w") as f:
            f.write("---------BILL-------\n")
            f.write(f"Invoice ID : {self.invoice_id}\n")
            f.write(f"Patient: {self.patient_name}\n")

            if self.insurance_company:
                f.write(f"Insurance: {self.insurance_company}\n")
                f.write(f"Coverage: {self.coverage_percent}\n")
            else:
                f.write("Insurance: None\n")
            
            f.write("Items:\n")
            for item in self.items:
                f.write(f" - {item.description} x{item.quantity} = {item.get_subtotal()}\n")
            
            total = self.get_total()
            insurance_part = self.get_insurance_covered_amount()
            patient_part = self.get_patient_payable()

            f.write(f"Total bill: {self.get_total()}\n")
            if self.insurance_company:
                f.write(f"Covered by insurance: {insurance_part}\n")
                f.write(f"Patient must pay: {patient_part}\n")
            f.write("----------------------\n")
