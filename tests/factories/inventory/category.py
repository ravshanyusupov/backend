from src.apps.inventory.models import Category
from tests.faker import fake

import factory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name_uz = fake.name()
    name_ru = fake.name()
