CRM Celery Setup Guide

This guide explains how to configure and run Celery, Celery Beat, and Redis for the CRM application. It covers installation, configuration, running tasks, and verifying logs.

Install Redis and Dependencies

Install Redis:

sudo apt update
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis

Install Python packages:

pip install celery django-celery-beat redis

Apply Django Migrations

Run migrations:

python manage.py migrate

Start Celery Worker

Start Celery worker from the folder containing manage.py:

celery -A crm worker -l info

Start Celery Beat Scheduler

Start celery beat in another terminal:

celery -A crm beat -l info

Verify Celery Report Task Logging

After the task runs, check the log file:

/tmp/crm_report_log.txt

Example log entry format:

YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue

Files Implemented in This Task

crm/celery.py
Initializes the Celery app with Redis as the broker.

crm/tasks.py
Contains the generate_crm_report Celery task that queries GraphQL and logs the CRM report.

crm/settings.py
Includes Celery configuration, Celery Beat schedule, and Redis broker setup.

crm/init.py
Ensures Celery app loads with Django.

Running the Full System

Start Django server:

python manage.py runserver

Start Redis:

redis-server

Start Celery worker:

celery -A crm worker -l info

Start Celery beat:

celery -A crm beat -l info

Expected Behavior

Celery Beat triggers generate_crm_report every Monday at 6:00 AM.

The task uses a GraphQL query to fetch:

Total customers

Total orders

Total revenue

It writes the report to:

/tmp/crm_report_log.txt

Place this file inside:
crm/README.md