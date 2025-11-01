# CRM Project Setup and Celery Tasks

This document explains how to set up the CRM project, run cron jobs, and configure Celery tasks for generating weekly reports.

---

## 1. Install Dependencies

Make sure you have Python 3, pip, and Redis installed.
Then install the project dependencies:

```bash
pip3 install -r requirements.txt
```

---

## 2. Run Django Migrations

Apply the database migrations:

```bash
python3 manage.py migrate
```

---

## 3. Schedule Cron Jobs

### 3.1 Clean Inactive Customers

* Cron job runs every Sunday at 2:00 AM.
* Logs deleted customers to `/tmp/customer_cleanup_log.txt`.

```bash
# Example to add manually
crontab crm/cron_jobs/customer_cleanup_crontab.txt
```

### 3.2 Order Reminders

* Cron job runs daily at 8:00 AM.
* Logs reminders to `/tmp/order_reminders_log.txt`.

```bash
crontab crm/cron_jobs/order_reminders_crontab.txt
```

### 3.3 Low Stock Products Update

* Cron job runs every 12 hours.
* Logs updated products to `/tmp/low_stock_updates_log.txt`.

---

## 4. Celery Setup

### 4.1 Install Celery and Beat

```bash
pip3 install celery django-celery-beat
```

Add `django_celery_beat` to `INSTALLED_APPS` in `crm/settings.py`.

---

### 4.2 Configure Celery

Create `crm/celery.py`:

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

app = Celery('crm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

Update `crm/__init__.py`:

```python
from .celery import app as celery_app

__all__ = ['celery_app']
```

---

### 4.3 Start Redis Server

Make sure Redis is running:

```bash
sudo service redis-server start
```

---

### 4.4 Run Celery Worker and Beat

Start the Celery worker:

```bash
celery -A crm worker -l info
```

Start Celery Beat:

```bash
celery -A crm beat -l info
```

---

### 4.5 Verify Logs

The weekly CRM report is logged to:

```
/tmp/crm_report_log.txt
```

Format:

```
YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
```

---

## 5. Notes

* Ensure the GraphQL endpoint `http://localhost:8000/graphql` is running before executing cron jobs or Celery tasks.
* Check `/tmp` logs to confirm tasks are executed properly.
* All cron jobs and Celery tasks are configured to run automatically based on
