from typing import Optional
from ninja import Schema
from pydantic import constr


class ResponsiblePersonPatchSchema(Schema):
    id: int
    first_name: Optional[constr(min_length=1, max_length=50, strip_whitespace=True)] = None
    last_name: Optional[constr(min_length=1, max_length=50, strip_whitespace=True)] = None
    middle_name: Optional[constr(min_length=1, max_length=50, strip_whitespace=True)] = None
    phone_number: Optional[constr(min_length=1, max_length=20, strip_whitespace=True)] = None
    work_place: Optional[constr(min_length=1, max_length=100, strip_whitespace=True)] = None
    passport_serial: Optional[constr(min_length=1, max_length=9, strip_whitespace=True)] = None
    job_title: Optional[constr(min_length=1, max_length=50, strip_whitespace=True)] = None
    order: Optional[constr(min_length=1, max_length=20, strip_whitespace=True)] = None
    date_of_order: Optional[constr(strip_whitespace=True)] = None
