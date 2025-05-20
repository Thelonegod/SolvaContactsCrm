import pytest

@pytest.mark.api
@pytest.mark.negative
def test_delete_nonexistent_contact(api_client):
    application_id = 28
    nonexistent_contact_id = 999999
    endpoint = f"/additional/{application_id}/contacts/{nonexistent_contact_id}"

    response = api_client(endpoint, method="DELETE")

    assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"

    data = response.json()
    assert "error" in data or "message" in data, "Ожидалось сообщение об ошибке в ответе"