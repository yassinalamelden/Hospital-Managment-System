import os
from backend.modules.staff_management import doctor
from backend.modules.staff_management import nurse

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
            
            # Save extra details if it's a doctor or nurse
            if isinstance(self, doctor):
                f.write(f"Specialization: {self.specialization}\n")
            elif isinstance(self, nurse):
                f.write(f"Shift: {self.shift}\n")
                
        print(f"--> Saved {self.name} to {filename}")
