# 📚 Library Service API

This is a REST API for a Library Management System built with Django and Django REST Framework. It allows managing books, users, and borrowings, and features automated Telegram notifications with Stripe payment integration.

## 🛠 Features Implemented So Far

- **Books Service**: Manage book inventory, titles, authors, cover types, and daily fees.
- **Users Service**: User registration, authentication (JWT tokens), and profile management.
- **Borrowings Service**: Create and manage book borrowings with validation (prevents borrowing if out of stock).
- **Telegram Notifications**: 
  - Instant alerts when a new borrowing is created.
  - Instant notifications when a book is successfully returned.
  - **Daily Overdue Task**: Automated check for late returns via Celery and Celery Beat.
- **Payments Service (Stripe Integration)**: 
  - Automated Stripe Checkout Session creation for every new borrowing.
  - Handling successful payments and canceling sessions.
  - Automatic status updates (`PENDING` -> `PAID`) in the database upon successful transaction.

---

## 🚀 Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/Viktor395/library-service-api.git
cd library-service-api

2. Set up virtual environment

python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt

3. Environment Variables
Create a `.env` file in the root directory and add the following keys (you can use `.env.sample` as a template):

DJANGO_SECRET_KEY=your_django_secret_key_here
DJANGO_DEBUG=True
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
STRIPE_PUBLIC_KEY=your_stripe_public_key_here
STRIPE_SECRET_KEY=your_stripe_secret_key_here
STRIPE_SUCCESS_URL=http://127.0.0.1:8000/api/payments/success/
STRIPE_CANCEL_URL=http://127.0.0.1:8000/api/payments/cancel/

4. Apply Migrations & Run Server

python manage.py migrate
python manage.py runserver

🐳 Running with Docker
If you prefer to run the entire infrastructure (Django with SQLite, Redis, and Celery) inside Docker containers, follow these steps:

1. Ensure you have Docker and Docker Compose installed.

2. Create and fill your .env file based on .env.sample.

3. Build and launch the containers using the following command in the root directory:

docker-compose up --build

This command automatically applies database migrations, starts the DRF web server on http://127.0.0.1:8000/, runs the Redis instance, and boots up both the Celery worker and Celery Beat scheduler in separate containers.



⏰ Background Tasks (Celery & Redis)
To run the automated background tasks (like daily overdue notifications), make sure Redis server is running, then start Celery components in separate terminal windows:

Run Celery Worker:
# For Windows:
celery -A library_config worker --loglevel=info -P threads
# For Linux/macOS:
celery -A library_config worker --loglevel=info

Run Celery Beat (Scheduler):

celery -A library_config beat --loglevel=info

## 🗺 API Endpoints for Payments

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/payments/` | List user's payments (or all for admin) | Authenticated |
| `GET` | `/api/payments/success/` | Stripe success callback (updates status to PAID) | Public |
| `GET` | `/api/payments/cancel/` | Stripe cancel callback | Public |
