from httpx import Response
from fastapi.testclient import TestClient
from fastapi import status
import pytest

from rwi_backend import schemas

def test_create_movie_success(
    authorized_client: TestClient,
):
    new_movie = {"title": "title", "year": 2000, "director": "director"}
    rwi_response: Response = authorized_client.post("/movie", json=new_movie)
    assert rwi_response.status_code == status.HTTP_201_CREATED

@pytest.mark.parametrize(
    "title, year, director", 
    [
        pytest.param(None, 2000, "director", id="missing title"),
        pytest.param("title", None, "director", id="missing year"),
        pytest.param("title", 2000, None, id="missing director"),
    ]
)
def test_create_movie_failure(
    authorized_client: TestClient,
    title, year, director
):
    new_movie = {"title": title, "year": year, "director": director}
    rwi_response: Response = authorized_client.post("/movie", json=new_movie)
    assert rwi_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_movie_conflict(
    authorized_client: TestClient,
    test_movie: schemas.MovieOut
):
    new_movie = {"title": test_movie.title, "year": test_movie.year, "director": test_movie.director}
    rwi_response: Response = authorized_client.post("/movie", json=new_movie)
    assert rwi_response.status_code == status.HTTP_409_CONFLICT

def test_create_movie_unauthorized(unauthorized_client: TestClient):
    new_movie = {"title": "title", "year": 2000, "director": "director"}
    rwi_response: Response = unauthorized_client.post("/movie", json=new_movie)
    assert rwi_response.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_movie_unauthorized(
    unauthorized_client: TestClient,
    test_movie: schemas.MovieOut
):
    new_movie = {"title": "title", "year": 2000, "director": "director"}
    rwi_response: Response = unauthorized_client.put(f"/movie/{test_movie}", json=new_movie)
    assert rwi_response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_movie(
    authorized_client: TestClient,
    test_movie: schemas.MovieOut
):
    rwi_response: Response = authorized_client.get(f"/movie/{test_movie.movie_id}")
    assert rwi_response.status_code == status.HTTP_200_OK

@pytest.mark.parametrize(
    "title, year, director, status_code", 
    [
        pytest.param("title1", 2000, "director", status.HTTP_200_OK, id="valid data"),
        pytest.param(None, 2000, "director", status.HTTP_422_UNPROCESSABLE_ENTITY, id="missing title"),
        pytest.param("title", None, "director", status.HTTP_422_UNPROCESSABLE_ENTITY, id="missing year"),
        pytest.param("title", 2000, None, status.HTTP_422_UNPROCESSABLE_ENTITY, id="missing director"),
        pytest.param("title", 2000, "director", status.HTTP_409_CONFLICT, id="movie exists")
    ]
)
def test_update_movie(
    authorized_client: TestClient,
    test_movie: schemas.MovieOut,
    title, year, director, status_code
):
    updated_movie = {"title": title, "year": year, "director": director}
    rwi_response: Response = authorized_client.put(f"/movie/{test_movie.movie_id}", json=updated_movie)
    assert rwi_response.status_code == status_code
    if rwi_response.status_code == status.HTTP_200_OK:
        updated_movie_response = schemas.MovieOut.model_validate(rwi_response.json())
        assert updated_movie_response.title == title
        assert updated_movie_response.year == year
        assert updated_movie_response.director == director

def test_delete_movie_unauthorized(
    unauthorized_client: TestClient,
    test_movie: schemas.MovieOut,
):
    rwi_response: Response = unauthorized_client.delete(f"/movie/{test_movie.movie_id}")
    assert rwi_response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_movie_authorized(
    authorized_client: TestClient,
    test_movie: schemas.MovieOut,
):
    rwi_response: Response = authorized_client.delete(f"/movie/{test_movie.movie_id}")
    assert rwi_response.status_code == status.HTTP_204_NO_CONTENT
    rwi_response: Response = authorized_client.delete(f"/movie/{test_movie.movie_id}")
    assert rwi_response.status_code == status.HTTP_404_NOT_FOUND