import pytest


@pytest.fixture
def product(product_factory):
    return product_factory.create()
