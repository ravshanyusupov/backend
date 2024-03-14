import pytest


@pytest.fixture
def product_norm_region(product_norm_factory):
    return product_norm_factory.create(district=None)


@pytest.fixture
def product_norm_district(product_norm_factory, region_user):
    return product_norm_factory.create(region=region_user.region)
