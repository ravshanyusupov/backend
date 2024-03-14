import logging, json

from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Add periodic tasks to run in the background"

    def add_statistics_tasks(self):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,  # every day
            period=IntervalSchedule.DAYS,
        )

        # Create the periodic task
        PeriodicTask.objects.get_or_create(
            task="src.apps.statistics.tasks.refresh_stats",
            defaults={
                "interval": schedule,
                "name": "Refresh stats task",
                "args": json.dumps([]),
                "kwargs": json.dumps(
                    {
                        "all": True,
                    }
                ),
            },
        )

    def handle(self, *args, **kwargs):
        self.add_statistics_tasks()
