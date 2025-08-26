# Pharmaceutical-Management-System
A full-stack Django-based Pharmaceutical Management System with role-based authentication for admin, along with real-time inventory tracking, product categorization, and automated billing workflows.

# Features
- User authentication (login, signup, logout)
- Medicine management (add, edit, delete medicines)
- Inventory management with stock details
- Bill generation and PDF download
- Bill history tracking
- Clean UI with templates and static resources

# Tech Stack
- Backend: Django 
- Database: SQLite 
- Frontend: HTML, CSS 
- Other: ReportLab (for PDF generation)

## Setup Instructions

Follow the steps below to set up the project on your local machine.

```bash
git clone https://github.com/tarung-15/Pharmaceutical-Management-System.git
cd Pharmaceutical-Management-System
python -m venv venv
venv\Scripts\activate  # (windows)
# source venv/bin/activate   (Linux/Mac)
pip install -r requirements.txt
pip install django reportlab arabic-reshaper python-bidi
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
# Open http://127.0.0.1:8000/ in your browser.
