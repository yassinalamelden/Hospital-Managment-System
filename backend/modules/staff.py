import os


class Staff:


    def __init__(self, id, name, age, password, department, salary):
        self.id = id
        self.name = name
        self.department = department
        
                                                   
        self.__age = age
        self.__password = password
        self.__salary = salary

    
    
    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, amount):
        if amount < 0:
            print("Error: Salary cannot be negative.")
        else:
            self.__salary = amount

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, new_age):
        if new_age < 18:
            print("Error: Staff must be at least 18 years old.")
        else:
            self.__age = new_age

       ##password authentication##
    def verify_password(self, input_pass):
        return self.__password == input_pass

    def change_password(self, old_pass, new_pass):
        # Check old password first
        if not self.verify_password(old_pass):
            print("Error: Old password verification failed.")
            return False
            
        # Check length of new password
        if len(new_pass) < 4:
            print("Error: New password must be at least 4 characters.")
            return False
            
        self.__password = new_pass
        print("Password updated successfully.")
        return True

    # GENERAL METHODS 

    def view_dashboard(self):

        print(f"Staff Dashboard: {self.name} | Dept: {self.department}")
### SAVE TO FILE 
    def save_to_file(self):
        """Saves staff details to a text file in the data folder."""
        os.makedirs("data/staff", exist_ok=True)
        filename = f"data/staff/{self.id}.txt"
        
        with open(filename, "w") as f:
            f.write(f"ID: {self.id}\n")
            f.write(f"Role: {self.__class__.__name__}\n")
            f.write(f"Name: {self.name}\n")
            f.write(f"Dept: {self.department}\n")
            f.write(f"Password: {self.__password}\n") # Saving pass for simple login
            
            # Save extra details if it's a Doctor or Nurse
            if isinstance(self, Doctor):
                f.write(f"Specialization: {self.specialization}\n")
            elif isinstance(self, Nurse):
                f.write(f"Shift: {self.shift}\n")
                
        print(f"--> Saved {self.name} to {filename}")

class Doctor(Staff):   ##inheritance#
    
    def __init__(self, id, name, age, password, department, salary, specialization):
    
        super().__init__(id, name, age, password, department, salary)

        self.specialization = specialization
        self.patient_list = []

    def view_dashboard(self):      # POLYMORPHISM Overriding the parent method
                                                    
        print(f"\n=== DOCTOR PORTAL ===")
        print(f"Dr. {self.name} ({self.specialization})")
        print(f"Assigned Patients: {len(self.patient_list)}")
        print("1. View Schedule")
        print("2. Prescribe Medication")

    def add_patient(self, patient_name):
        self.patient_list.append(patient_name)
        print(f"Patient {patient_name} added to Dr. {self.name}'s list.")

    def prescribe_medication(self, patient_name, medicine):
        if patient_name in self.patient_list:
            print(f"Prescribed {medicine} to {patient_name}.")
        else:
            print(f"Error: {patient_name} is not your patient.")


class Nurse(Staff):   
   
    def __init__(self, id, name, age, password, department, salary, shift):
        super().__init__(id, name, age, password, department, salary)
        self.shift = shift  
        self.rooms = []

    def view_dashboard(self):
        # POLYMORPHISM##
        print(f"\n=== NURSE STATION ===")
        print(f"Nurse {self.name} | Shift: {self.shift}")
        print(f"Assigned Rooms: {', '.join(self.rooms)}")

    def assign_room(self, room_number):
        self.rooms.append(room_number)
        print(f"Nurse {self.name} assigned to Room {room_number}.")


class Admin(Staff):

    def view_dashboard(self):
        print(f"\n=== ADMINISTRATOR CONTROL ===")
        print(f"Admin: {self.name}")
        print("1. View All Staff")
        print("2. Payroll System")

    def update_salary(self, staff_member, new_amount):
        print(f"Updating salary for {staff_member.name}")
        staff_member.salary = new_amount
        print(f"New salary set to: {staff_member.salary}")