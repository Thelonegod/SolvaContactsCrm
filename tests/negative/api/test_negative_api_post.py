import pytest

@pytest.mark.api
@pytest.mark.negative
def test_post_contact_invalid_payload(api_client):
    endpoint = "/additional/28/contacts"
    invalid_payload = {
        "fullName": "",
        "position": "Manager",
        "contactMethods": {},
        "comment": "Test comment",
        "contactType": "PRIMARY"
    }

    response = api_client(endpoint, method="POST", json=invalid_payload)


    assert response.status_code in (400, 422), f"Ожидался 400 или 422, получен {response.status_code}"


    data = response.json()
    assert "error" in data or "message" in data, "В ответе отсутствует сообщение об ошибке"
