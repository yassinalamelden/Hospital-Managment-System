from .staff import doctor, nurse, admin

class StaffManager:
    def __init__(self):
        self.staff_list = []
        self.current_user = None

    def hire_doctor(self, id, name, age, password, spec, salary):
        # Check if the ID is already used
        if self.check_id(id):
            print("Error: This ID already exists.")
            return

        # Create new doctor instance
        new_doc = doctor(id, name, age, password, "Medical", salary, spec)
        
        self.staff_list.append(new_doc)
        new_doc.save_to_file() 
        print(f"Dr. {name} hired successfully.")

    def hire_nurse(self, id, name, age, password, shift, salary):
        if self.check_id(id):
            print("Error: This ID already exists.")
            return

        new_nurse = nurse(id, name, age, password, "Nursing", salary, shift)
        
        self.staff_list.append(new_nurse)
        new_nurse.save_to_file()
        print(f"Nurse {name} hired successfully.")

    def check_id(self, id):
        for staff in self.staff_list:
            if staff.id == id:
                return True
        return False

    def login(self, id, password):
        for staff in self.staff_list:
            if staff.id == id:
                if staff.verify_password(password):
                    self.current_user = staff
                    print(f"Welcome back, {staff.name}")
                    return True
        return False

    def logout(self):
        self.current_user = None