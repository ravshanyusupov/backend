from src.apps.dictionary.models import ResponsiblePerson
from django.contrib.auth import get_user_model
from ninja_lib.error import DomainException

User = get_user_model()


async def check_district_of_instance(responsible_person: ResponsiblePerson, user: User):
    if not responsible_person.district_id == user.district_id:
        raise DomainException(3000)
