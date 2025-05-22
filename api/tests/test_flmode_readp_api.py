import pytest

@pytest.mark.usefixtures("db")
class TestFlModelRead:
    def test_list_requires_auth(self, api_client):
        resp = api_client.get("/api/models/")
        assert resp.status_code == 401

    def test_list_with_token(self, api_client, token):
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        resp = api_client.get("/api/models/")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_detail_requires_auth(self, api_client, model):
        resp = api_client.get(f"/api/models/{model.id}/")
        assert resp.status_code == 401

    def test_detail_nonexistent(self, api_client, token):
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        resp = api_client.get("/api/models/9999/")
        assert resp.status_code == 404

    def test_detail_success(self, api_client, token, model):
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        resp = api_client.get(f"/api/models/{model.id}/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == model.id
        assert data["name"] == model.name
        assert pytest.approx(data["accuracy"], rel=1e-3) == model.accuracy
        assert pytest.approx(data["generalisability"], rel=1e-3) == model.generalisability
        assert pytest.approx(data["privacy"], rel=1e-3) == model.privacy
