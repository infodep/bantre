from .conftest import TestClient, client_fixture


def test_client(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}