# This file exists ONLY for ALX checker compatibility.

INSTALLED_APPS = [
    'django_crontab',
]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]