from datetime import datetime as dt
from fastapi.testclient import TestClient
from fastapi import status
from httpx import Response
import pytest
from typing import Any
from rwi_backend import schemas


@pytest.mark.parametrize(
    "email, username, password, status_code",
    [
        pytest.param(
            "email@domain.com",
            "username",
            "password",
            status.HTTP_201_CREATED,
            id="valid data",
        ),
        pytest.param(
            None,
            "username",
            "password",
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            id="missing email",
        ),
        pytest.param(
            "email@domain.com",
            None,
            "password",
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            id="missing username",
        ),
        pytest.param(
            "email@domain.com",
            "username",
            None,
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            id="missing password",
        ),
    ],
)
def test_user_registration(
    authorized_client: TestClient,
    email: str | None,
    username: str | None,
    password: str | None,
    status_code: int,
) -> None:
    json_data = {"email": email, "username": username, "password": password}
    rwi_response: Response = authorized_client.post("/auth/register", json=json_data)
    assert rwi_response.status_code == status_code
    if status_code == 201:
        registration_data: schemas.UserOut = schemas.UserOut(**rwi_response.json())
        assert registration_data.email == email
        assert registration_data.username == username
        assert isinstance(registration_data.created_at, dt)


def test_user_correct_login(
    authorized_client: TestClient, test_user: schemas.UserOut
) -> None:
    json_data = {"username": "testemail@domain.com", "password": "testpassword"}
    rwi_response: Response = authorized_client.post("/auth/login", data=json_data)
    assert rwi_response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        pytest.param(
            None, "password", status.HTTP_422_UNPROCESSABLE_CONTENT, id="missing email"
        ),
        pytest.param(
            "testemail@domain.com",
            None,
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            id="missing password",
        ),
        pytest.param(
            "testemail@domain.com",
            "pwd",
            status.HTTP_401_UNAUTHORIZED,
            id="invalid credentials",
        ),
    ],
)
def test_user_incorrect_login(
    authorized_client: TestClient,
    email: str | None,
    password: str | None,
    status_code: int,
    request: Any,
) -> None:
    data: dict[str, str] = {"username": email or "", "password": password or ""}
    rwi_response: Response = authorized_client.post("/auth/login", data=data)
    assert rwi_response.status_code == status_code
    if request.node.callspec.id.startswith("missing"):
        assert rwi_response.json().get("detail")[0].get("type") == "missing"
    else:
        assert rwi_response.json().get("detail") == "Invalid credentials"
