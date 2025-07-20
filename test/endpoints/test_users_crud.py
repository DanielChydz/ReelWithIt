from fastapi.testclient import TestClient
from fastapi import status
from httpx import Response
from rwi_backend import schemas
import pytest

def test_read_user_authorized(
    authorized_client: TestClient,
    test_user: schemas.UserOut
):
    rwi_response: Response = authorized_client.get(f"/user/{test_user.username}")
    assert rwi_response.status_code == status.HTTP_200_OK

def test_read_user_unauthorized(
    unauthorized_client: TestClient,
    test_user: schemas.UserOut
):
    rwi_response: Response = unauthorized_client.get(f"/user/{test_user.username}")
    assert rwi_response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.parametrize(
    "email, username, password, status_code",
    [
        pytest.param("newemail@domain.com", "newusername", "newpassword", status.HTTP_200_OK, id="valid data"),
        pytest.param(None, "newusername", "newpassword", status.HTTP_422_UNPROCESSABLE_ENTITY, id="missing email"),
        pytest.param("newemail@domain.com", None, "newpassword", status.HTTP_422_UNPROCESSABLE_ENTITY, id="missing username"),
        pytest.param("newemail@domain.com", "newusername", None, status.HTTP_422_UNPROCESSABLE_ENTITY, id="missing password")
    ]
)
def test_update_user_authorized(
    authorized_client: TestClient,
    test_user: schemas.UserOut,
    email, username, password, status_code
):
    updated_user = {"email": email, "username": username, "password": password}
    rwi_response: Response = authorized_client.put(f"/user/{test_user.username}", json=updated_user)
    assert rwi_response.status_code == status_code

def test_update_user_unauthorized(
    unauthorized_client: TestClient,
    test_user: schemas.UserOut,
):
    updated_user = {"email": "email@domain.com", "username": "username", "password": "password"}
    rwi_response: Response = unauthorized_client.put(f"/user/{test_user.username}", json=updated_user)
    assert rwi_response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_user_authorized(
    authorized_client: TestClient,
    test_user: schemas.UserOut,
):
    rwi_response: Response = authorized_client.delete(f"/user/{test_user.username}")
    assert rwi_response.status_code == status.HTTP_204_NO_CONTENT
    rwi_response: Response = authorized_client.delete(f"/user/{test_user.username}")
    assert rwi_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_user_unauthorized(
    unauthorized_client: TestClient,
    test_user: schemas.UserOut,
):
    rwi_response: Response = unauthorized_client.delete(f"/user/{test_user.username}")
    assert rwi_response.status_code == status.HTTP_401_UNAUTHORIZED