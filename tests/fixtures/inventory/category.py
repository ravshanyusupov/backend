import pytest


@pytest.fixture
def fake_category(category_factory):
    return category_factory.create()
