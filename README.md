# 📚 Library Service API

This is a REST API for a Library Management System built with Django and Django REST Framework. It allows managing books, users, and borrowings, and features automated Telegram notifications.

## 🛠 Features Implemented So Far

- **Books Service**: Manage book inventory, titles, authors, cover types, and daily fees.
- **Users Service**: User registration, authentication (JWT tokens), and profile management.
- **Borrowings Service**: Create and manage book borrowings with validation (prevents borrowing if out of stock).
- **Telegram Notifications**: 
  - Instant alerts when a new borrowing is created.
  - Instant notifications when a book is successfully returned.
  - **Daily Overdue Task**: Automated check for late returns via Celery and Celery Beat.

---

## 🚀 Installation & Setup

1. Clone the repository

```bash
git clone https://github.com/Viktor395/library-service-api.git
cd library-service-api

2. Set up virtual environment

python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt

3. Environment Variables
Create a .env file in the root directory and add the following keys:

SECRET_KEY=your_django_secret_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
STRIPE_SECRET_KEY=your_stripe_test_secret_key

4. Apply Migrations & Run Server

python manage.py migrate
python manage.py runserver

⏰ Background Tasks (Celery & Redis)
To run the automated background tasks (like daily overdue notifications), make sure Redis server is running, then start Celery components in separate terminal windows:

Run Celery Worker:
# For Windows:
celery -A library_config worker --loglevel=info -P threads
# For Linux/macOS:
celery -A library_config worker --loglevel=info

Run Celery Beat (Scheduler):

celery -A library_config beat --loglevel=info
