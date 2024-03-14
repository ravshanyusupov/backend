import factory

from tests.faker import fake

from src.apps.dictionary.models import Region


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Region

    name_ru = fake.name()
    name_uz = fake.name()
