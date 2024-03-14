from django.conf import settings
from celery import Celery
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("uscs_app")
app.config_from_object("django.conf:settings")
app.conf.broker_url = settings.CELERY_BROKER_URL


app.autodiscover_tasks()
