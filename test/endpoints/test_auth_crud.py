from datetime import datetime as dt
from fastapi.testclient import TestClient
from fastapi import status
from httpx import Response
import pytest
from rwi_backend import schemas

@pytest.mark.parametrize(
    "email, username, password, status_code",
    [
        pytest.param("email@domain.com", "username", "password", status.HTTP_201_CREATED, id="valid data"),
        pytest.param(None, "username", "password", status.HTTP_422_UNPROCESSABLE_ENTITY, id="missing email"), 
        pytest.param("email@domain.com", None, "password", status.HTTP_422_UNPROCESSABLE_ENTITY, id="missing username"),
        pytest.param("email@domain.com", "username", None, status.HTTP_422_UNPROCESSABLE_ENTITY, id="missing password")
    ]
)
def test_user_registration(
    authorized_client: TestClient,
    email, username, password, status_code
):
    json_data = {"email": email, "username": username, "password": password}
    rwi_response: Response = authorized_client.post("/auth/register", json=json_data)
    assert rwi_response.status_code == status_code
    if status_code == 201:
        registration_data: schemas.UserOut = schemas.UserOut(**rwi_response.json())
        assert registration_data.email == email
        assert registration_data.username == username
        assert isinstance(registration_data.created_at, dt)

def test_user_correct_login(authorized_client: TestClient, test_user):
    json_data = {"username": "testemail@domain.com", "password": "testpassword"}
    rwi_response: Response = authorized_client.post("/auth/login", data=json_data)
    assert rwi_response.status_code == 200

@pytest.mark.parametrize(
    "email, password, status_code", 
    [
        pytest.param(None, "password", status.HTTP_403_FORBIDDEN, id="missing email"),
        pytest.param("testemail@domain.com", None, status.HTTP_403_FORBIDDEN, id="missing email")
    ]
)
def test_user_incorrect_login(authorized_client: TestClient, email, password, status_code):
    json_data = {"username": email, "password": password}
    rwi_response: Response = authorized_client.post("/auth/login", data=json_data)
    assert rwi_response.status_code == status_code
    assert rwi_response.json().get("detail") == "Invalid credentials"