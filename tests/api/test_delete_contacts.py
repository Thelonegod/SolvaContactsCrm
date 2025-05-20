import pytest

@pytest.mark.api
@pytest.mark.positive
def test_delete_contact(api_client, created_contact_id):
    application_id = 28
    contact_id = created_contact_id
    endpoint = f"/additional/{application_id}/contacts/{contact_id}"

    response = api_client(endpoint, method="DELETE")

    assert response.status_code == 200
    assert response.text == ''
