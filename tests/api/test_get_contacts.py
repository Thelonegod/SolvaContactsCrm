import pytest

@pytest.mark.api
@pytest.mark.positive
def test_get_contacts(api_client):
    response = api_client("/additional/28/contacts")

    assert response.status_code == 200, f"Ошибка: {response.status_code}"

    data = response.json()
    assert data, "Ответ пустой"
    print("Успех! Данные:", data)