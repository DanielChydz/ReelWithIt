from httpx import Response
from fastapi import status
from fastapi.testclient import TestClient
from rwi_backend import schemas
import pytest

def test_add_rating_success(authorized_client: TestClient, test_movie: schemas.MovieOut):
    rwi_response: Response = authorized_client.post(f"/rating/{test_movie.movie_id}", json={"rating": 8})
    assert rwi_response.status_code == status.HTTP_200_OK
    response = schemas.RatingOutPersonal.model_validate(rwi_response.json())
    assert response.rating == 8

@pytest.mark.parametrize(
    "rating", 
    [
        pytest.param(0, id="too low rating"),
        pytest.param(1.11, id="too precise rating"),
        pytest.param(10.1, id="too high rating"),
    ]
)
def test_add_rating_failure(authorized_client: TestClient, test_movie: schemas.MovieOut, rating):
    rwi_response: Response = authorized_client.post(f"/rating/{test_movie.movie_id}", json={"rating": rating})
    assert rwi_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_add_rating_duplicate(authorized_client: TestClient, test_movie: schemas.MovieOut):
    authorized_client.post(f"/rating/{test_movie.movie_id}", json={"rating": 5})
    rwi_response: Response = authorized_client.post(f"/rating/{test_movie.movie_id}", json={"rating": 6})
    assert rwi_response.status_code == status.HTTP_409_CONFLICT

def test_add_rating_movie_not_found(authorized_client: TestClient):
    rwi_response: Response = authorized_client.post(f"/rating/9999999", json={"rating": 7})
    assert rwi_response.status_code == status.HTTP_404_NOT_FOUND

def test_add_rating_unauthorized(unauthorized_client: TestClient, test_movie: schemas.MovieOut):
    rwi_response: Response = unauthorized_client.post(f"/rating/{test_movie.movie_id}", json={"rating": 5})
    assert rwi_response.status_code == status.HTTP_401_UNAUTHORIZED

def test_read_rating_success(authorized_client: TestClient, test_movie: schemas.MovieOut):
    authorized_client.post(f"/rating/{test_movie.movie_id}", json={"rating": 5})
    rwi_response: Response = authorized_client.get(f"/rating/{test_movie.movie_id}")
    assert rwi_response.status_code == status.HTTP_200_OK
    rating = schemas.RatingOut.model_validate(rwi_response.json())
    assert isinstance(rating.rating, float)
    assert rating.movie_id == test_movie.movie_id

def test_read_rating_movie_not_found(authorized_client: TestClient):
    rwi_response: Response = authorized_client.get(f"/rating/9999")
    assert rwi_response.status_code == status.HTTP_409_CONFLICT

def test_update_rating_success(authorized_client: TestClient, test_movie: schemas.MovieOut):
    authorized_client.post(f"/rating/{test_movie.movie_id}", json={"rating": 5})
    rwi_response: Response = authorized_client.patch(f"/rating/{test_movie.movie_id}", json={"rating": 9})
    assert rwi_response.status_code == status.HTTP_200_OK
    updated_rating = schemas.RatingOutPersonal.model_validate(rwi_response.json())
    assert updated_rating.rating == 9

def test_update_rating_not_found(authorized_client: TestClient, test_movie: schemas.MovieOut):
    rwi_response: Response = authorized_client.patch(f"/rating/{test_movie.movie_id}", json={"rating": 6})
    assert rwi_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_rating_success(authorized_client: TestClient, test_movie: schemas.MovieOut):
    authorized_client.post(f"/rating/{test_movie.movie_id}", json={"rating": 7})
    rwi_response: Response = authorized_client.delete(f"/rating/{test_movie.movie_id}")
    assert rwi_response.status_code == status.HTTP_204_NO_CONTENT
    rwi_response = authorized_client.delete(f"/rating/{test_movie.movie_id}")
    assert rwi_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_rating_unauthorized(unauthorized_client: TestClient, test_movie: schemas.MovieOut):
    rwi_response: Response = unauthorized_client.delete(f"/rating/{test_movie.movie_id}")
    assert rwi_response.status_code == status.HTTP_401_UNAUTHORIZED
