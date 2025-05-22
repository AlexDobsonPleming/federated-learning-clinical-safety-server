# tests/test_localmodel_api.py
import pytest
from rest_framework import status
from api.models import LocalModel

@pytest.mark.django_db
class TestLocalModelAPI:
    @property
    def list_url(self):
        return lambda model_id: f"/api/models/{model_id}/locals/"

    @property
    def detail_url(self):
        return lambda model_id, local_id: f"/api/models/{model_id}/locals/{local_id}/"

    # --- LIST tests ---

    def test_list_requires_auth(self, api_client, model):
        resp = api_client.get(self.list_url(model.id))
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_empty(self, api_client, token, model):
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        resp = api_client.get(self.list_url(model.id))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == []

    def test_list_with_items(self, api_client, token, model):
        # create two local models under the same fl_model
        LocalModel.objects.create(
            fl_model=model,
            name="LM1",
            privacy=0.1,
            leakage_chance=0.01,
            noise=0.05
        )
        LocalModel.objects.create(
            fl_model=model,
            name="LM2",
            privacy=0.2,
            leakage_chance=0.02,
            noise=0.06
        )

        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        resp = api_client.get(self.list_url(model.id))
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert isinstance(data, list)
        # Only check that names are present
        assert {item["name"] for item in data} == {"LM1", "LM2"}

    # --- DETAIL tests ---

    def test_detail_requires_auth(self, api_client, model):
        lm = LocalModel.objects.create(
            fl_model=model,
            name="LM",
            privacy=0.3,
            leakage_chance=0.03,
            noise=0.07
        )
        resp = api_client.get(self.detail_url(model.id, lm.id))
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_detail_not_found(self, api_client, token, model):
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        resp = api_client.get(self.detail_url(model.id, 9999))
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_detail_success(self, api_client, token, model):
        lm = LocalModel.objects.create(
            fl_model=model,
            name="LM",
            privacy=0.4,
            leakage_chance=0.04,
            noise=0.08
        )
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        resp = api_client.get(self.detail_url(model.id, lm.id))
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert data["id"] == lm.id
        assert data["name"] == lm.name
        assert pytest.approx(data["privacy"], rel=1e-3) == lm.privacy
        assert pytest.approx(data["leakage_chance"], rel=1e-3) == lm.leakage_chance
        assert pytest.approx(data["noise"], rel=1e-3) == lm.noise

    # --- CREATE tests ---

    def test_create_requires_auth(self, api_client, model):
        payload = {
            "name": "NewLM",
            "privacy": 0.5,
            "leakage_chance": 0.05,
            "noise": 0.09
        }
        resp = api_client.post(self.list_url(model.id), data=payload, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_machine_user_can_create(self, api_client, machine_token, model):
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {machine_token.key}")
        payload = {
            "name": "NewLM",
            "privacy": 0.6,
            "leakage_chance": 0.06,
            "noise": 0.10
        }
        resp = api_client.post(self.list_url(model.id), data=payload, format="json")
        assert resp.status_code == status.HTTP_201_CREATED

        data = resp.json()
        assert data["name"] == payload["name"]
        assert pytest.approx(data["privacy"], rel=1e-3) == payload["privacy"]
        assert pytest.approx(data["leakage_chance"], rel=1e-3) == payload["leakage_chance"]
        assert pytest.approx(data["noise"], rel=1e-3) == payload["noise"]

    # --- UPDATE tests ---

    def test_update_requires_auth(self, api_client, model):
        lm = LocalModel.objects.create(
            fl_model=model,
            name="Old",
            privacy=0.7,
            leakage_chance=0.07,
            noise=0.11
        )
        payload = {"privacy": 0.75}
        resp = api_client.patch(self.detail_url(model.id, lm.id), data=payload, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_machine_user_can_update(self, api_client, machine_token, model):
        lm = LocalModel.objects.create(
            fl_model=model,
            name="Old",
            privacy=0.8,
            leakage_chance=0.08,
            noise=0.12
        )
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {machine_token.key}")
        payload = {
            "name": "Updated",
            "privacy": 0.85,
            "leakage_chance": 0.088,
            "noise": 0.13
        }
        resp = api_client.patch(self.detail_url(model.id, lm.id), data=payload, format="json")
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert data["name"] == "Updated"
        assert pytest.approx(data["privacy"], rel=1e-3) == 0.85
        assert pytest.approx(data["leakage_chance"], rel=1e-3) == 0.088
        assert pytest.approx(data["noise"], rel=1e-3) == 0.13

    # --- DELETE tests ---

    def test_delete_requires_auth(self, api_client, model):
        lm = LocalModel.objects.create(
            fl_model=model,
            name="ToDelete",
            privacy=0.9,
            leakage_chance=0.09,
            noise=0.14
        )
        resp = api_client.delete(self.detail_url(model.id, lm.id))
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_machine_user_can_delete(self, api_client, machine_token, model):
        lm = LocalModel.objects.create(
            fl_model=model,
            name="ToDelete",
            privacy=0.95,
            leakage_chance=0.095,
            noise=0.15
        )
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {machine_token.key}")
        resp = api_client.delete(self.detail_url(model.id, lm.id))
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # verify it’s gone
        assert not LocalModel.objects.filter(id=lm.id).exists()
