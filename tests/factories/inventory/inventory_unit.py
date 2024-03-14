import datetime

import factory

from tests.faker import fake

from src.apps.inventory.models import InventoryUnit
from tests.factories.inventory import ProductFactory
from tests.factories.dictionary import StoragePlaceFactory, DistrictFactory


class InventoryUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InventoryUnit

    product = factory.SubFactory(ProductFactory)
    storage_place = factory.SubFactory(StoragePlaceFactory)
    district = factory.SubFactory(DistrictFactory)
    commissioning_year = 2020
    inventory_number = factory.Sequence(lambda n: "Inventory %03d" % n)
