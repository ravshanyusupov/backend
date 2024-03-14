from asgiref.sync import sync_to_async
from src.apps.dictionary.models import ResponsiblePerson


@sync_to_async
def get_responsible_persons(filter_conditions):
    queryset = ResponsiblePerson.objects.filter(
        filter_conditions
    ).only("first_name", "last_name", "middle_name", "passport_serial")

    return list(queryset)