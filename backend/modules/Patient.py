class Patient:
    def __init__(self , name , age , blood_type , Id , gender , phone , address ):
        self.name = name
        self.age = age
        self.blood_type = blood_type
        self.Id = Id
        self.gender = gender
        self.phone = phone
        self.address = address
        #intialization of attributes 
        self.medical_history = []
        self.current_medications = []
        self.allergies = []
        self.current_diagnosis = None
#creating extra features  to the patient 
    def update_phone(self, new_phone):
        self.phone = new_phone

    def update_address(self, new_address):
        self.address = new_address

    def add_allergy(self, allergy):
        if allergy not in self.allergies:
            self.allergies.append(allergy)
    #this helps us to update somethings in patient like phone or address or allegry 
    def add_medical_history(self, record):
        self.medical_history.append(record)
    #a method helps to add to the empty list created above a new medical history 
    def add_medication(self, medication):
        self.current_medications.append(medication)
    # a method that adds a new medication to patient 
    def get_full_record(self):
        return {
            "Patient ID": self.Id,
            "Name": self.name,
            "Age": self.age,
            "Gender": self.gender,
            "Blood Type": self.blood_type,
            "Phone": self.phone,
            "Address": self.address,
            "Allergies": self.allergies,
            "Medical History": self.medical_history,
            "Current Medications": self.current_medications
        }
    # this method is used to display the full info of the patient 