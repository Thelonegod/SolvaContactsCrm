import pytest

@pytest.mark.api
@pytest.mark.positive
def test_post_contact(api_client):
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
    assert response.text == ''  # потому что ответ пустой по документации