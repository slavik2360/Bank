# Python
import os

# Third party
from celery import Celery
from celery.schedules import crontab

# Django
from django.conf import settings


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'settings.base'
)
app = Celery(
    'settings',
    broker=settings.CELERY_BROKER_URL
)
app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)
app.autodiscover_tasks(
    lambda: settings.PROJECT_APPS
)

## Запус каждый день в 0:00
app.conf.beat_schedule = {
    'every_day_at_00': {
        'task': 'bank.tasks.delete_expired_cards',
        'schedule': crontab(minute=0, hour=0),
    },
}
## Запус каждую миуну
# app.conf.beat_schedule = {
#     'every_1_minute': {
#         'task': 'bank.tasks.delete_expired_cards',
#         'schedule': crontab(minute='*/1'),
#     },
# }
app.conf.timezone = 'UTC'