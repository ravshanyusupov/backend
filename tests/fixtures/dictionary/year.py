import pytest


@pytest.fixture
def year(year_factory):
    instance = year_factory.create()

    return instance
