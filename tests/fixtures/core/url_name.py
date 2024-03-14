import pytest
from django.urls import reverse_lazy
from config.urls import URL_NAMESPACE


@pytest.fixture
def url_name():
    return lambda file_name: reverse_lazy(
        URL_NAMESPACE
        + ":"
        + file_name.partition("tests")[2]
        .replace("/", ".")
        .replace(".py", "")
        .replace("test_", "")[1:]
    )
