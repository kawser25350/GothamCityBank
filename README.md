# GothamCity Bank

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/Status-Educational%20Project-C8A15A)](#security-notice)

**Repository:** [github.com/kawser25350/Bank_Managment_System](https://github.com/kawser25350/Bank_Managment_System)
**Demo:** Run locally with the instructions below. No public demo is currently configured.

## Overview

GothamCity Bank is a Django banking management application for customer accounts, everyday transactions, loan approval, and account activity reporting.

It combines a customer-facing banking workspace with Django admin controls for transaction and loan management.

## Screenshots

The current interface includes responsive views for:

- Public banking homepage
- Authenticated customer dashboard
- Profile and account centre
- Deposit, withdrawal, transfer, and loan forms
- Transaction ledger and filters
- Django admin loan approval

Screenshots are not committed to the repository yet. Add them under `docs/screenshots/` when preparing a portfolio or interview presentation.

## Features

- Customer registration, login, logout, and profile updates
- Savings and Regular account types
- Account balance and account number management
- Deposits and withdrawals with validation
- Transfers between bank accounts
- Loan requests with administrator approval
- One-time balance credit when a loan is approved
- Loan repayment from the transaction ledger
- Transaction filtering by date and type
- HTML and plain-text transaction email notifications
- Django admin transaction management
- Responsive desktop and mobile interface

## Tech Stack

- **Backend:** Python, Django 6.1
- **Database:** SQLite for local development
- **Forms:** Django Crispy Forms and Crispy Bootstrap 5
- **Frontend:** Django templates, HTML, CSS, and JavaScript
- **Email:** Django SMTP with Gmail app-password authentication
- **Assets:** Django static files and Pillow
- **Configuration:** Python Decouple

## Architecture / Application Flow

```text
Browser
  |
  v
Django URL routes
  |
  +--> Accounts app
  |      +--> registration and authentication
  |      +--> profile and address management
  |      +--> UserBank_account records
  |
  +--> Transactions app
  |      +--> deposit, withdrawal, and transfer workflows
  |      +--> loan request and repayment workflows
  |      +--> transaction ledger and filters
  |      +--> confirmation email service
  |
  +--> Core app
         +--> public and authenticated home pages
         +--> shared navigation, footer, and static styling

                         |
                         v
                    SQLite database

Django admin ---> loan approval ---> account balance update
```

### Main application boundaries

- `accounts/` owns users, bank accounts, addresses, registration, authentication, and profiles.
- `transactions/` owns transaction forms, balance mutations, loan workflows, reports, email notifications, and admin approval.
- `core/` owns the home page, shared layout, static assets, and visual system.
- `bank_managment/` contains project settings, root URLs, WSGI, and ASGI configuration.

## Key Technical Highlights

- Uses class-based Django views and shared transaction form/view abstractions.
- Validates deposits, withdrawals, transfers, and loan limits before processing.
- Uses database transactions and row locking during loan repayment.
- Credits an approved loan only on the approval transition to prevent duplicate balance updates.
- Uses Django admin as the approval surface for staff workflows.
- Sends multipart emails with HTML template content and a plain-text fallback.
- Includes responsive navigation, mobile layouts, structured forms, and an activity visualization.
- Includes regression coverage for the one-time loan approval balance update.

## Project Structure

```text
Bank_managment_System/
├── accounts/                 # Users, accounts, addresses, profiles
├── bank_managment/           # Django project configuration
├── core/                     # Home page, shared templates, static files
├── transactions/             # Banking operations, reports, loan workflows
├── db.sqlite3                # Local SQLite database
├── manage.py                 # Django management commands
├── requirements.txt          # Python dependencies
└── README.md
```

## Requirements

- Python 3.12 or newer
- pip
- Git

## Installation

Clone the repository:

```bash
git clone https://github.com/kawser25350/Bank_Managment_System.git
cd Bank_Managment_System
```

Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv env
env\Scripts\Activate.ps1
```

Install dependencies and apply migrations:

```bash
pip install -r requirements.txt
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open the application at `http://127.0.0.1:8000/`.
Open the admin panel at `http://127.0.0.1:8000/admin/`.

## Email Configuration

Transaction notifications use Gmail SMTP. Create a `.env` file in the project root:

```env
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

Use a Gmail app password, not a normal Gmail password. Never commit `.env`, passwords, or exported user data.

## Testing

Run Django checks:

```bash
python manage.py check
```

Run the test suite:

```bash
python manage.py test
```

## Loan Approval Flow

1. A customer submits a loan request.
2. The request appears in Django admin as pending.
3. An administrator approves the request.
4. The approved amount is added to the account balance once.
5. The customer repays the loan from the transaction ledger.

## Database

The current project uses SQLite:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

SQLite is suitable for local development and demonstrations. A persistent PostgreSQL database should be configured before handling real production data.

## Deployment Notes

The project can be deployed to a service such as Render for a demonstration. Render web-service filesystems are not persistent by default, so SQLite data can be lost after redeployments or restarts.

Before production deployment:

- Move `SECRET_KEY` to an environment variable.
- Set `DEBUG = False`.
- Configure `ALLOWED_HOSTS` and CSRF trusted origins.
- Use persistent PostgreSQL storage.
- Configure production static-file serving.
- Store email credentials as platform environment variables.
- Enable HTTPS and database backups.

## Security Notice

This is an educational banking management project. It is not ready to process real financial data without a professional security review, persistent production storage, audit logging, stronger authorization controls, rate limiting, and compliance work.

## License

Not specified.
