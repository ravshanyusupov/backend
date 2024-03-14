from src.apps.inventory.models import Product
from tests.factories.inventory import CategoryFactory
from tests.faker import fake

import factory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name_uz = fake.name()
    name_ru = fake.name()
    category = factory.SubFactory(CategoryFactory)
