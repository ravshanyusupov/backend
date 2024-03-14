import pytest


@pytest.fixture
def region(region_factory):
    region_factory.create()
