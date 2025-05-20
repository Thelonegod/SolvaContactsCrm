# файл: conftest.py

import pytest
import requests
from requests.auth import HTTPBasicAuth

@pytest.fixture(scope="session")
def api_client():
    base_url = "https://front-crm-lab-master.k8s.dev.solvatech.kz/api/back/partner"

    auth = HTTPBasicAuth("Df323Ds7232sdhU", "fJllcMtdRUEYu91bsFUQ")

    def make_request(endpoint, method="GET", **kwargs):
        url = f"{base_url}{endpoint}"
        response = requests.request(method, url, auth=auth, **kwargs)
        return response

    return make_request

import pytest

@pytest.fixture(scope="module")
def created_contact_id(api_client):
    endpoint = "/additional/28/contacts"
    payload = {
        "fullName": "Раян Гослинг",
        "position": "Manager",
        "contactMethods": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        },
        "comment": "Test comment",
        "contactType": "PRIMARY"
    }

    response = api_client(endpoint, method="POST", json=payload)
    assert response.status_code == 200
    assert response.text == ''

    contacts = api_client(endpoint).json()
    contact = next(c for c in contacts if c.get("fullName") == payload["fullName"])
    contact_id = contact["id"]

    yield contact_id
