from django.test import Client
import json, pytest


DEFAULT_CONTENT_TYPE = "application/json"


class APIClient(Client):
    def post(self, path, data=None, content_type=DEFAULT_CONTENT_TYPE, **extra):
        if data and content_type == DEFAULT_CONTENT_TYPE:
            data = json.dumps(data)
        return super().post(path, data, content_type, **extra)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def cec_client(cec_login):
    return APIClient(headers={"Authorization": f"Bearer {cec_login['access']}"})


@pytest.fixture
def region_client(region_login):
    return APIClient(headers={"Authorization": f"Bearer {region_login['access']}"})


@pytest.fixture
def district_client(district_login):
    return APIClient(headers={"Authorization": f"Bearer {district_login['access']}"})
