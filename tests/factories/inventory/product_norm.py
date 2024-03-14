from src.apps.inventory.models import ProductNorm
from tests.factories.inventory import ProductFactory
from tests.factories.dictionary import RegionFactory, DistrictFactory
from tests.faker import fake

import factory


class ProductNormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductNorm

    product = factory.SubFactory(ProductFactory)
    region = factory.SubFactory(RegionFactory)
    district = factory.SubFactory(DistrictFactory)
