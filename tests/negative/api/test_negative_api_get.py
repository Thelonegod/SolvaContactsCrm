import pytest

@pytest.mark.api
@pytest.mark.negative
def test_get_contacts_not_found(api_client):
    response = api_client("/additional/999999/contacts")

    assert response.status_code == 404, f"Ожидался 404, но получен {response.status_code}"

    data = response.json()
    assert "error" in data or "message" in data, "В ответе отсутствует сообщение об ошибке"