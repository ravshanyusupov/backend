import factory
from tests.faker import fake
from src.apps.dictionary.models.building_category import BuildingCategory


class BuildingCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BuildingCategory

    name_uz = fake.name()
    name_ru = fake.name()
