import pytest

@pytest.mark.api
@pytest.mark.positive
def test_put_update_contact(api_client, created_contact_id):
    application_id = 28
    contact_id = created_contact_id
    endpoint = f"/additional/{application_id}/contacts/{contact_id}"

    payload = {
        "fullName": "Стив из Майнкрафта",
        "position": "Team Lead",
        "contactMethods": {
            "additionalProp1": "value1",
            "additionalProp2": "value2",
            "additionalProp3": "value3"
        },
        "comment": "Updated contact info",
        "contactType": "PRIMARY"
    }

    response = api_client(endpoint, method="PUT", json=payload)

    assert response.status_code == 200
    assert response.text == ''
