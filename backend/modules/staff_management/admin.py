from backend.modules.staff_management import Staff

class admin(Staff):

    def view_dashboard(self):
        print(f"\n=== adminISTRATOR CONTROL ===")
        print(f"admin: {self.name}")
        print("1. View All Staff")
        print("2. Payroll System")

    def update_salary(self, staff_member, new_amount):
        print(f"Updating salary for {staff_member.name}")
        staff_member.salary = new_amount
        print(f"New salary set to: {staff_member.salary}")