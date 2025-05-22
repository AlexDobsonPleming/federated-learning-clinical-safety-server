import pytest

@pytest.mark.usefixtures("db")
class TestFlModelWrite:
    def test_upload_requires_auth(self, api_client):
        payload = {
            "name": "ShouldFail",
            "accuracy": 0.9,
            "generalisability": 0.9,
            "privacy": 0.9,
        }
        resp = api_client.post("/api/models/", data=payload, format="json")
        assert resp.status_code == 401

    def  test_machine_user_can_upload(self, api_client, machine_token):
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {machine_token.key}")
        payload = {
            "name": "UploadedModel",
            "accuracy": 0.92,
            "generalisability": 0.89,
            "privacy": 0.8,
        }
        resp = api_client.post("/api/models/", data=payload, format="json")
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == payload["name"]
        assert pytest.approx(data["accuracy"], rel=1e-3) == payload["accuracy"]
        assert pytest.approx(data["generalisability"], rel=1e-3) == payload["generalisability"]
        assert pytest.approx(data["privacy"], rel=1e-3) == payload["privacy"]
