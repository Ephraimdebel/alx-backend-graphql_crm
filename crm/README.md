# CRM Celery Report Setup

## Install Redis and dependencies
```
pip3 install -r requirements.txt
sudo service redis-server start

```
## Run Django Migrations

python3 manage.py migrate

## Start Celery Worker

celery -A crm worker -l info
## Start Celery Beat

celery -A crm beat -l info
## Verify Logs
Check /tmp/crm_report_log.txt for weekly CRM reports.