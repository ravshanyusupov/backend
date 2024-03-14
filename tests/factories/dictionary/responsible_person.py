import factory

from tests.faker import fake

from src.apps.dictionary.models import ResponsiblePerson
from tests.factories.dictionary import RegionFactory, DistrictFactory


class ResponsiblePersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResponsiblePerson

    first_name = fake.first_name()
    last_name = fake.last_name()
    middle_name = fake.first_name()
    phone_number = "+9989700000000"
    work_place = fake.job()
    passport_serial = factory.Sequence(lambda n: "%03d" % n)
    job_title = fake.name()
    order = str(fake.pyint())
    date_of_order = fake.date_time()

    region = factory.SubFactory(RegionFactory)
    district = factory.SubFactory(DistrictFactory)
