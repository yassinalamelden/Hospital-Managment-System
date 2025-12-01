from datetime import date
from Role import Role
import re
from abc import ABC, abstractmethod


class User(ABC):
    def __init__(
        self,
        user_id,
        username,
        password,
        first_name,
        last_name,
        birth_date,
        ssn,
        phone_number,
        email,
        address,
        role,
    ):
        self.__id = user_id
        self.__userName = username
        self.__password = password
        self.__firstName = first_name
        self.__lastName = last_name
        self.__birthDate = birth_date
        self.__ssn = ssn
        self.__phoneNumber = phone_number
        self.__email = email
        self.__address = address
        self.__role = role

    @staticmethod
    def create(
        user_id,
        username,
        password,
        ssn, 
        role_string,
        first_name = "",
        last_name = "",
        birth_date = None,
        phone_number = "",
        email="",
        address="",
    ):
        
        if not user_id or not user_id.strip():
            raise ValueError("User ID is required and cannot be empty.")
        if not username or not username.strip():
            raise ValueError("Username is required and cannot be empty.")
        if not password:
            raise ValueError("Password is required.")
        if not ssn or not ssn.strip():
            raise ValueError("SSN is required.")
        if not role_string or not role_string.strip():
            raise ValueError("Role is required.")
            
        if len(password) < 8 or not re.search(r"\d", password):
            raise ValueError("Password must be at least 8 characters long and contain at least one digit.")

        if not re.match(r"^\d{3}-?\d{2}-?\d{4}$", ssn.strip()):
            raise ValueError("SSN format is invalid. Use XXX-XX-XXXX or XXXXXXXXX.")
        
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")

        if phone_number and not re.match(r"^[\d\s\-\(\)\+]*$", phone_number):
            raise ValueError("Invalid characters in phone number.")

        final_birth_date = None
        if birth_date is not None:
            if isinstance(birth_date, date):
                final_birth_date = birth_date
            elif isinstance(birth_date, str):
                try:
                    final_birth_date = date.fromisoformat(birth_date) 
                except ValueError:
                    raise ValueError("Birth Date string must be in 'YYYY-MM-DD' format.")
            else:
                raise TypeError("Birth Date must be a 'datetime.date' object or a 'YYYY-MM-DD' string.")

            if final_birth_date >= date.today():
                raise ValueError("Birth Date cannot be today or in the future.")

        try:
            role_obj = Role.create_role(role_string)
        except ValueError as e:
            raise ValueError(f"Role Validation Error: {e}") from e

        return User(
            user_id.strip(),
            username.strip(),
            password,
            first_name.strip(),
            last_name.strip(),
            final_birth_date,
            ssn.strip(),
            phone_number.strip(),
            email.strip(),
            address.strip(),
            role_obj
        )
    
    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.__birthDate.year
            - (
                (today.month, today.day)
                < (self.__birthDate.month, self.__birthDate.day)
            )
        )

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__userName

    @property
    def password(self):
        return self.__password

    @property
    def first_name(self):
        return self.__firstName

    @property
    def last_name(self):
        return self.__lastName

    @property
    def full_name(self):
        return f"{self.__firstName} {self.__lastName}"

    @property
    def birth_date(self):
        return self.__birthDate

    @property
    def ssn(self):
        return self.__ssn

    @property
    def phone_number(self):
        return self.__phoneNumber

    @property
    def email(self):
        return self.__email

    @property
    def address(self):
        return self.__address

    @property
    def role(self):
        return self.__role

    @property
    def age(self):
        if self.__birthDate is None:
            return None
        today = date.today()
        return (
            today.year
            - self.__birthDate.year
            - (
                (today.month, today.day)
                < (self.__birthDate.month, self.__birthDate.day)
            )
        )
    
    def get_contact_info(self):
        return f"Phone: {self.phone_number} | Email: {self.email} | Address: {self.address}"

    def is_adult(self):
        if self.age is None:
            return False 
        return self.age >= 18
    
    def validate_password(self,password):
        return self.__password == password
    
    @abstractmethod
    def get_unique_id(self):
        pass

    @abstractmethod
    def get_entity_type(self):
        pass

    @abstractmethod
    def display_record_summary(self):
        pass

    @abstractmethod
    def link_to_medical_record(self, record_id):
        pass