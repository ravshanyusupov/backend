from celery import shared_task
from django.core import management

from django_celery_beat.models import PeriodicTask, IntervalSchedule
import logging, json

from src.apps.core.management.commands import refresh_statistics

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s %(message)s", level=logging.INFO
)


@shared_task
def refresh_stats(*args, **kwargs):
    management.call_command(refresh_statistics.Command(), *args, **kwargs)
    logging.info(f"Stats task has been completed.")
