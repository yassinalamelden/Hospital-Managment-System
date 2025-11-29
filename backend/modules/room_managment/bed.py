class Bed:
    '''
    For Individule Beds
    '''
    def __init__(self, bed_id):
        self.bed_id = bed_id
        self.is_avaliable = True
        self.patient_id = None

    def assign(self, patient_id):
        self.is_avaliable = False
        self.patient_id = patient_id

    def release(self):
        self.is_avaliable = True
        self.patient_id = None
        