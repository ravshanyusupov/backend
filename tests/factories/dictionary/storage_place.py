import factory
from tests.faker import fake
from src.apps.dictionary.models import StoragePlace
from tests.factories.dictionary import BuildingCategoryFactory, DistrictFactory


class StoragePlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StoragePlace

    address = fake.name()
    building_category = factory.SubFactory(BuildingCategoryFactory)
    district = factory.SubFactory(DistrictFactory)
