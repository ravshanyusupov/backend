import pytest


@pytest.fixture
def district(region, district_factory):
    district_factory.create(region=region)
