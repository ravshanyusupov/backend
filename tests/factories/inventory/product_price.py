from src.apps.inventory.models import ProductPrice
from tests.factories.inventory import ProductFactory
from tests.factories.dictionary import YearFactory
from tests.faker import fake

import factory


class ProductPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductPrice

    price = 100000
    product = factory.SubFactory(ProductFactory)
    year = factory.SubFactory(YearFactory)
