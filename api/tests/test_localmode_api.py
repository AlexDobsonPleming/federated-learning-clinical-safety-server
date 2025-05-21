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
        LocalModel.objects.create(fl_model=model, name="LM1", relatability=0.5, source="S1")
        LocalModel.objects.create(fl_model=model, name="LM2", relatability=0.6, source="S2")
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        resp = api_client.get(self.list_url(model.id))
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert isinstance(data, list)
        assert {item["name"] for item in data} == {"LM1", "LM2"}

    # --- DETAIL tests ---

    def test_detail_requires_auth(self, api_client, model):
        lm = LocalModel.objects.create(fl_model=model, name="LM", relatability=0.7, source="SX")
        resp = api_client.get(self.detail_url(model.id, lm.id))
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_detail_not_found(self, api_client, token, model):
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        resp = api_client.get(self.detail_url(model.id, 9999))
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_detail_success(self, api_client, token, model):
        lm = LocalModel.objects.create(fl_model=model, name="LM", relatability=0.7, source="SX")
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        resp = api_client.get(self.detail_url(model.id, lm.id))
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert data["id"] == lm.id
        assert data["name"] == lm.name
        assert pytest.approx(data["relatability"], rel=1e-3) == lm.relatability
        assert data["source"] == lm.source

    # --- CREATE tests ---

    def test_create_requires_auth(self, api_client, model):
        payload = {"name": "NewLM", "relatability": 0.8, "source": "SRC"}
        resp = api_client.post(self.list_url(model.id), data=payload, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_machine_user_can_create(self, api_client, machine_token, model):
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {machine_token.key}")
        payload = {"name": "NewLM", "relatability": 0.8, "source": "SRC"}
        resp = api_client.post(self.list_url(model.id), data=payload, format="json")
        assert resp.status_code == status.HTTP_201_CREATED

        data = resp.json()
        assert data["name"] == payload["name"]
        assert pytest.approx(data["relatability"], rel=1e-3) == payload["relatability"]
        assert data["source"] == payload["source"]

    # --- UPDATE tests ---

    def test_update_requires_auth(self, api_client, model):
        lm = LocalModel.objects.create(fl_model=model, name="Old", relatability=0.5, source="X")
        payload = {"name": "Updated"}
        resp = api_client.patch(self.detail_url(model.id, lm.id), data=payload, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_machine_user_can_update(self, api_client, machine_token, model):
        lm = LocalModel.objects.create(fl_model=model, name="Old", relatability=0.5, source="X")
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {machine_token.key}")
        payload = {"name": "Updated", "relatability": 0.55}
        resp = api_client.patch(self.detail_url(model.id, lm.id), data=payload, format="json")
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert data["name"] == "Updated"
        assert pytest.approx(data["relatability"], rel=1e-3) == 0.55

    # --- DELETE tests ---

    def test_delete_requires_auth(self, api_client, model):
        lm = LocalModel.objects.create(fl_model=model, name="ToDelete", relatability=0.1, source="Z")
        resp = api_client.delete(self.detail_url(model.id, lm.id))
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_machine_user_can_delete(self, api_client, machine_token, model):
        lm = LocalModel.objects.create(fl_model=model, name="ToDelete", relatability=0.1, source="Z")
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {machine_token.key}")
        resp = api_client.delete(self.detail_url(model.id, lm.id))
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # verify it’s gone
        assert not LocalModel.objects.filter(id=lm.id).exists()
