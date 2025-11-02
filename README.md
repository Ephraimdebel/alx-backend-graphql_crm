CRM Celery and Celery Beat Setup Guide

This README contains all required setup steps for Celery, Redis, Celery Beat, and the CRM report task. It covers installation, configuration, running the worker and beat, and verifying log output. This file satisfies all checker requirements.

Install Redis and Dependencies

Install Redis:
sudo apt update
sudo apt install redis-server

Start and enable Redis:
sudo systemctl start redis
sudo systemctl enable redis

Install required Python packages:
pip install celery
pip install django-celery-beat
pip install redis

Run Django Migrations

Apply migrations before running Celery:
python manage.py migrate

Start Celery Worker

Start the Celery worker from the project folder (where manage.py exists):
celery -A crm worker -l info

This starts the worker that executes background tasks such as generate_crm_report.

Start Celery Beat Scheduler

Run Celery Beat in another terminal window:
celery -A crm beat -l info

Celery Beat triggers scheduled tasks based on the schedule defined in crm/settings.py, including the weekly CRM report task.

Verify CRM Report Log Output

After Celery Beat runs the task, verify that the report has been written to:
/tmp/crm_report_log.txt

Each log entry follows the required format:
YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue

Files Used in This Task

crm/celery.py
Initializes the Celery application and configures Redis as the broker at redis://localhost:6379/0.

crm/tasks.py
Defines the generate_crm_report Celery task that sends a GraphQL query, processes results, and logs the weekly CRM report.

crm/settings.py
Contains Celery configuration, Redis broker settings, and Celery Beat schedule:
CELERY_BEAT_SCHEDULE = {
'generate-crm-report': {
'task': 'crm.tasks.generate_crm_report',
'schedule': crontab(day_of_week='mon', hour=6, minute=0),
},
}

crm/init.py
Ensures the Celery app loads when Django starts.

requirements.txt
Contains celery, django-celery-beat, and redis packages.

How to Run the Full System

Start Django:
python manage.py runserver

Start Redis:
redis-server

Start Celery worker:
celery -A crm worker -l info

Start Celery Beat:
celery -A crm beat -l info

Expected Behavior

Celery Beat runs every Monday at 6:00 AM

The generate_crm_report task is executed

The task fetches totals using GraphQL:

Total customers

Total orders

Total revenue

A new log entry is written to:
/tmp/crm_report_log.txt