# Hospital Management System

A comprehensive web-based application designed to streamline hospital operations, including patient management, appointment scheduling, billing, and staff administration. Built using the Django framework.
<img width="1917" height="924" alt="image" src="https://github.com/user-attachments/assets/35cb2c2a-3869-4669-89fb-e254b55ba9e2" />

## Features

### 🔐 Authentication & User Management
*   **User Roles**: Separation of database access for Superusers (Admins), Doctors, and Patients.
*   **Sign Up/Login**: Secure account creation and authentication system.
*   **Profile Management**: Update personal information, passwords, and account settings.

### 🏥 Patient Portal
*   **Dashboard**: Personalized dashboard for patients to view their status.
*   **Book Appointments**: Easy-to-use interface for scheduling appointments with doctors.
*   **Appointment History**: View past and upcoming appointments (`My Appointments`).
*   **Doctor Search**: Search for doctors by specialization or name.
*   **Room Availability**: Check for available hospital rooms for admission.
*   **Reviews**: Leave feedback and reviews for doctors and hospital services.

### 👨‍⚕️ Doctor & Admin Dashboard
*   **Doctor Management**: Admins can add, edit, delete, and toggle the active status of doctors.
*   **Patient Management**: Admins can oversee patient records, update details, or remove users.
*   **Appointment Oversight**: View and manage all hospital appointments.
*   **Review Management**: Admins can moderate user reviews.

### 🏨 Hospital Operations
*   **Room Management**:
    *   **Add/Edit Rooms**: Manage room inventory (Types: PSU, ICU, General, etc.).
    *   **Assign Rooms**: Assign specific rooms to patients.
    *   **Vacate Rooms**: Mark rooms as available after patient discharge.
    *   **Availability**: Track occupied vs. available rooms.
*   **Appointment Logic**: Complex logic for scheduling, preventing double-booking, and managing time slots.

### 💰 Billing System
*   **Invoice Generation**: Create bills for patients based on services and room usage.
*   **Bill Tracking**: Track the status of bills (Paid/Unpaid/Pending).
*   **Bill Items**: Detailed breakdown of charges within a single bill.

## Tech Stack

*   **Backend**: Python 3.x, Django 5.x
*   **Database**: SQLite (Default)
*   **Frontend**: HTML5, CSS3, JavaScript (Django Template Engine)
*   **Styling**: Custom CSS & Bootstrap (if applicable)

## Installation

Follow these steps to set up the project locally.

### Prerequisites

*   Python 3.8 or higher installed.

### Steps

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yassinalamelden/Hospital-Managment-System.git
    cd Hospital-Managment-System
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser** (for Admin access):
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server**:
    ```bash
    python manage.py runserver
    ```

7.  Open your browser and navigate to `http://127.0.0.1:8000/`.

## File Structure & Explanation

Here is a detailed breakdown of the project files and directories:

### 📁 Root Directory
*   `manage.py`: Django's command-line utility for administrative tasks.
*   `db.sqlite3`: The database file.
*   `requirements.txt`: List of Python dependencies.
*   `cleanup_bills.py`: detailed script to perform maintenance on billing records.
*   `verify_billing.py`: Script to verify and validate billing data integrity.

### 📁 accounts/
*Handles user authentication, doctor profiles, and patient data.*
*   `models/`:
    *   `doctor.py`: Defines the `Doctor` model (specialization, schedule).
    *   `patient.py`: Defines the `Patient` model (medical history, details).
    *   `person.py`: Abstract base class for user information.
*   `views/`:
    *   `auth_views.py`: Login, Logout, Signup logic.
    *   `client_views.py`: Views for the patient portal (booking, reviews, profile).
    *   `admin_views.py`: Views for admin dashboards and user management.
    *   `doctor_views.py`: Views specific to doctor actions.
*   `urls.py`: Routing for authentication and account pages.
*   `forms.py`: Forms for user registration, profile updates, and doctor creation.

### 📁 operations/
*Manages core hospital logistics like appointments and rooms.*
*   `models/`:
    *   `appointment.py`: Defines `Appointment` model.
    *   `room.py`: Defines `Room` model (type, number, availability).
    *   `review.py`: Defines `Review` model for feedback.
*   `views/`:
    *   Views for listing, creating, and updating appointments and rooms.
    *   Logic for vacating and assigning rooms.
*   `urls.py`: Routing for rooms and appointments.

### 📁 billing/
*Handles financial transactions and invoicing.*
*   `models/`:
    *   `bill.py`: Main `Bill` model linking patient, date, and total.
    *   `bill_item.py`: Individual items within a bill (e.g., specific test or medicine).
*   `urls.py`: Routing for bill management.
*   `views.py`: Logic for generating and viewing bills.

### 📁 config/
*Project-wide settings and configuration.*
*   `settings.py`: Main configuration (DB, Apps, Middleware, Static files).
*   `urls.py`: Main URL router (includes urls from other apps).
*   `asgi.py` / `wsgi.py`: Entry points for web servers.

### 📁 core/
*Shared utilities and main dashboard logic.*
*   `views.py`: Views for the main Admin Dashboard and shared components.

### 📁 templates/
*Contains HTML files for the frontend.*
*   Organized by app (`accounts`, `operations`, `billing`) and contains `base.html` for layout inheritance.

### 📁 static/
*   Contains CSS stylesheets, JavaScript files, and images used in the application.
