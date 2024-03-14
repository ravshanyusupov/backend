import factory

from tests.faker import fake

from src.apps.dictionary.models import District
from tests.factories.dictionary import RegionFactory


class DistrictFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = District

    name_ru = fake.name()
    name_uz = fake.name()
    region = factory.SubFactory(RegionFactory)
