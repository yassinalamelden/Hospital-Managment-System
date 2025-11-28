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

    def __init__(self, invoice_id, patient_name):
        self.invoice_id = invoice_id
        self.patient_name = patient_name
        self.items = []

    def add_item(self, description, quantity, price):
        item = InvoiceItem(description, quantity, price)
        self.items.append(item)

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
        print("Items: ")
        for item in self.items:
            print(f" - {item.description} x{item.quantity} = {item.get_subtotal()}")
        print(f"Total bill: {self.get_total()}")
        print("----------------------")

    def save_to_file(self, filename):
        """
        Saves the bill to a text file.
        """
        with open(filename, "w") as f:
            f.write("---------BILL-------\n")
            f.write(f"Invoice ID : {self.invoice_id}\n")
            f.write(f"Patient: {self.patient_name}\n")
            f.write("Items:\n")
            for item in self.items:
                f.write(f" - {item.description} x{item.quantity} = {item.get_subtotal()}\n")
            f.write(f"Total bill: {self.get_total()}\n")
            f.write("----------------------\n")
