from backend.modules.staff_management import Staff

class Doctor(Staff):   ##inheritance#
    
    def __init__(self, id, name, age, password, department, salary, specialization):
    
        super().__init__(id, name, age, password, department, salary)

        self.specialization = specialization
        self.patient_list = []

    def view_dashboard(self):      # POLYMORPHISM Overriding the parent method
                                                    
        print(f"\n=== doctor PORTAL ===")
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
            