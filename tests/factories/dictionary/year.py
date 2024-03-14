import factory

from tests.faker import fake
from src.apps.dictionary.models import Year


class YearFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Year

    year = fake.year()
