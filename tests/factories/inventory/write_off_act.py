import factory

from tests.faker import fake

from src.apps.inventory.models import WriteOffAct
from tests.factories.inventory import ProductFactory
from tests.factories.dictionary import RegionFactory, DistrictFactory


class WriteOffActFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WriteOffAct

    region = factory.SubFactory(RegionFactory)
    district = factory.SubFactory(DistrictFactory)
