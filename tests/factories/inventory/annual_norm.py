from tests.factories.inventory.product_norm import ProductNormFactory
from tests.factories.dictionary.year import YearFactory
from src.apps.inventory.models import AnnualNorm

import factory


class AnnualNormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AnnualNorm

    product_norm = factory.SubFactory(ProductNormFactory)
    year = factory.SubFactory(YearFactory)
    count = 10000
