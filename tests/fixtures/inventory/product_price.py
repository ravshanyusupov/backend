import pytest


@pytest.fixture
def product_price(product_price_factory):
    return product_price_factory.create()
