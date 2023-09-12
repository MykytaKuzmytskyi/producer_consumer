# Producer - Consumer

A simple service in which Celery adds an entry to the model once a minute, and after some time the user needs to delete these entries from the table in the browser by clicking on the appropriate button.

### Installing using GitHub

Install PostgresSQL and create db

1. Clone the source code:

```bash
git clone https://github.com/Thirteenthskyi/producer_consumer.git
cd producer_consumer
```

2. Install PostgresSQL and create DB.
3. Install modules and dependencies:

```bash
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

4. `.env_sample`
   This is a sample .env file for use in local development.
   Duplicate this file as .env in the root of the project
   and update the environment variables to match your
   desired config. You can use [djecrety.ir](https://djecrety.ir/)

5. Use the command to configure the database and tables:

```bash
python manage.py migrate
```

6. Run Redis server.

7. Run celery for tasks handling:

```bash
celery -A library_service worker -l info
```
8. Run Celery beat for task scheduling:

```bash
celery -A producer_consumer beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

9. Start the app:

```bash
python manage.py runserver
```

### Run with docker
Copy .env_sample -> .env and populate with all required data

Docker should be installed

```commandline
docker-compose up --build
```

### Getting access
1. Follow to the admin page and login `http://127.0.0.1:8000/admin/`
- You can use following superuser:
    - Login: `admin`
    - Password: `admin`

2. Follow this link to test the application `http://127.0.0.1:8000/orders/`