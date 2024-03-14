import factory

from tests.faker import fake

from src.apps.users.models import User
from tests.factories.dictionary import RegionFactory, DistrictFactory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class CecUserFactory(UserFactory):
    user_type = "C"
    username = fake.name()
    password = fake.password()


class RegionUserFactory(UserFactory):
    user_type = "R"
    username = fake.name()
    password = fake.password()
    region = factory.SubFactory(RegionFactory)


class DistrictUserFactory(UserFactory):
    user_type = "D"
    username = fake.name()
    password = fake.password()
    region = factory.SubFactory(RegionFactory)
    district = factory.SubFactory(DistrictFactory)
