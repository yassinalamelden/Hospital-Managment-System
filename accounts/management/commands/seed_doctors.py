import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from accounts.models.doctor import Doctor

class Command(BaseCommand):
    help = 'Seeds the database with Doctor records'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        specialties = [choice[0] for choice in Doctor.SPECIALTY_CHOICES]
        
        first_names_male = ['Ahmed', 'Omar', 'Khaled', 'Mahmoud', 'Mostafa', 'Amr', 'Yasser', 'Hany', 'Islam', 'Tarek', 'Karim', 'Ibrahim', 'Hossam', 'Ayman', 'Mohamed']
        first_names_female = ['Mona', 'Sara', 'Aya', 'Heba', 'Dina', 'Reem', 'Salma', 'Farah', 'Mariam', 'Yasmin', 'Nada', 'Rania', 'Laila', 'Nour', 'Fatima']
        last_names = ['Ali', 'Hassan', 'Ibrahim', 'Mohamed', 'Youssef', 'Adel', 'Fathy', 'Nabil', 'Salah', 'Kamal', 'Samir', 'Lotfy', 'Reda', 'Ashraf', 'Farid']
        
        doctors_created = 0
        
        for _ in range(50):
            gender = random.choice(['Male', 'Female'])
            if gender == 'Male':
                first_name = random.choice(first_names_male)
            else:
                first_name = random.choice(first_names_female)
                
            last_name = random.choice(last_names)
            name = f"{first_name} {last_name}"
            
            age = random.randint(28, 65)
            # Create a somewhat realistic Egyptian-style phone number or generic 10-digit
            phone = f"01{random.randint(0, 2)}{random.randint(10000000, 99999999)}"
            address = f"{random.randint(1, 999)} Main St, City {random.randint(1, 20)}"
            specialty = random.choice(specialties)
            fee = Decimal(random.randint(50, 500))
            
            Doctor.objects.create(
                name=name,
                age=age,
                gender=gender,
                phone=phone,
                address=address,
                specialty=specialty,
                consultation_fee=fee,
                is_active=True
            )
            doctors_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {doctors_created} doctors'))
