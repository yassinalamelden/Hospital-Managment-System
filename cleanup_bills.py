from billing.models import Bill
from decimal import Decimal

bills = Bill.objects.all()
count = 0
for b in bills:
    if b.doctor_fees > 0 and b.items.filter(item_name__icontains='Consultation').exists():
        b.doctor_fees = Decimal('0.00')
        b.save()
        count += 1

print(f"CLEANED: {count} bills with duplicate consultation fees")
