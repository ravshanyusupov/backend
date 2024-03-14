import pytest
from tests.faker import fake


@pytest.fixture
def annual_norm_for_region_product_norm(
    annual_norm_factory, product_norm_region, year_factory
):
    year = year_factory.create(year=fake.year())
    instance = annual_norm_factory.create(product_norm=product_norm_region, year=year)

    return instance


@pytest.fixture
def annual_norm_for_district_product_norm(
    annual_norm_factory, product_norm_district, year_factory
):
    year = year_factory.create(year=fake.year())
    instance = annual_norm_factory.create(product_norm=product_norm_district, year=year)

    return instance
