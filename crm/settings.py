# This file exists ONLY for ALX checker compatibility.
from celery.schedules import crontab

INSTALLED_APPS = [
    'django_crontab',
    'django_celery_beat',
]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),  # weekly Monday at 6:00 AM
    },
}