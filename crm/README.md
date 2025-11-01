# CRM Project - Background Tasks and Reporting

This project demonstrates the integration of background tasks, cron jobs, and GraphQL queries/mutations in a Django CRM application. It includes customer cleanup, order reminders, stock updates, and weekly CRM report generation using Celery.

## Requirements

* Python 3.12+
* Django
* django-crontab
* celery
* django-celery-beat
* gql
* Redis (for Celery broker)
* GraphQL endpoint ([http://localhost:8000/graphql](http://localhost:8000/graphql))

## Setup

1. **Install dependencies**

```bash
pip3 install -r requirements.txt
```

Ensure the following are included in `requirements.txt`:

```
django-crontab
celery
django-celery-beat
gql
requests
```

2. **Database Migrations**

```bash
python3 manage.py migrate
```

3. **Configure Cron Jobs**

* **Customer Cleanup**: Runs every Sunday at 2:00 AM

```python
('0 2 * * 0', 'crm.cron.clean_inactive_customers')
```

* **Order Reminders**: Runs daily at 8:00 AM

```python
('0 8 * * *', 'crm.cron.send_order_reminders')
```

* **Low Stock Update**: Runs every 12 hours

```python
('0 */12 * * *', 'crm.cron.update_low_stock')
```

4. **Configure Celery with Beat**

* In `crm/settings.py`, add:

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'

INSTALLED_APPS += [
    'django_celery_beat',
]

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
```

* Initialize Celery in `crm/celery.py`:

```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
app = Celery('crm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

* Load Celery app in `crm/__init__.py`:

```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

5. **Running Services**

* Start Django server:

```bash
python3 manage.py runserver
```

* Start Celery worker:

```bash
celery -A crm worker -l info
```

* Start Celery Beat scheduler:

```bash
celery -A crm beat -l info
```

6. **Verify Logs**

* Customer cleanup: `/tmp/customer_cleanup_log.txt`
* Order reminders: `/tmp/order_reminders_log.txt`
* Heartbeat: `/tmp/crm_heartbeat_log.txt`
* Low stock updates: `/tmp/low_stock_updates_log.txt`
* Weekly CRM report: `/tmp/crm_report_log.txt`

7. **GraphQL Queries & Mutations**

* `hello` query: Verifies the endpoint is alive.
* `UpdateLowStockProducts` mutation: Updates products with stock < 10.
* Custom queries for reports and customer/order filtering are available at `/graphql`.

## Notes

* Ensure Redis is running locally for Celery.
* Cron jobs rely on `django-crontab` to schedule tasks.
* Logs are stored in `/tmp` for demonstration purposes; adjust paths in production.
* GraphQL endpoint should be ac
