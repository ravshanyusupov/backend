from ninja import Schema
from pydantic import constr
from src.apps.dictionary.models import ResponsiblePerson


class CreateResponsiblePersonSchema(Schema):
    first_name: constr(min_length=1, max_length=50, strip_whitespace=True)
    last_name: constr(min_length=1, max_length=50, strip_whitespace=True)
    middle_name: constr(min_length=1, max_length=50, strip_whitespace=True)
    phone_number: constr(min_length=1, max_length=20, strip_whitespace=True)
    work_place: constr(min_length=1, max_length=100, strip_whitespace=True)
    passport_serial: constr(min_length=1, max_length=9, strip_whitespace=True)
    job_title: constr(min_length=1, max_length=50, strip_whitespace=True)
    order: constr(min_length=1, max_length=20, strip_whitespace=True)
    date_of_order: constr(strip_whitespace=True)
