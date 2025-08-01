from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from rwi_backend import models, schemas
from rwi_backend.database import get_db
from rwi_backend.oauth2 import get_current_user_auth
from rwi_backend.utils import AddRating, RemoveRating, UpdateRating

router = APIRouter(
    prefix="/rating",
    tags=["ratings"]
)

@router.post("/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.RatingOutPersonal)
def add_rating(
    movie_id: int,
    rating: schemas.RatingAdd,
    db: Annotated[Session, Depends(get_db)],
    current_user: schemas.UserOut = Depends(get_current_user_auth)
):
    
    existing_movie: models.Movies | None = db.query(models.Movies).filter_by(movie_id=movie_id).first()
    if existing_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id {movie_id} does not exist")
    existing_rating: models.Ratings | None = db.query(models.Ratings).filter_by(user_id=current_user.user_id,
                                                        movie_id=movie_id).first()
    if existing_rating:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.user_id} has already rated movie with id {movie_id}")
    new_rating = models.Ratings(user_id=current_user.user_id,
                                movie_id=movie_id,
                                rating=rating.rating)
    db.add(new_rating)
    existing_movie.rating = AddRating(existing_movie.rating,
                                      existing_movie.number_of_ratings,
                                      rating.rating)
    existing_movie.number_of_ratings += 1
    db.commit()
    db.refresh(new_rating)
    rating_out = schemas.RatingOutPersonal.model_validate({
        "rating": new_rating.rating,
        "movie_id": new_rating.movie_id,
        "title": existing_movie.title,
        "number_of_ratings": existing_movie.number_of_ratings,
        "user_id": new_rating.user_id
    })
    return rating_out

@router.get("/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.RatingOut)
def read_rating(
    movie_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> schemas.RatingOut:
    
    movie: models.Movies | None = db.query(models.Movies).filter(models.Movies.movie_id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"movie with id {movie_id} does not exist")
    rating = schemas.RatingOut.model_validate(movie)
    return rating

@router.patch("/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.RatingOutPersonal)
def update_rating(
    movie_id: int,
    rating: schemas.RatingAdd,
    db: Annotated[Session, Depends(get_db)],
    current_user: schemas.UserOut = Depends(get_current_user_auth)
):
    
    existing_movie: models.Movies | None = db.query(models.Movies).filter_by(movie_id=movie_id).first()
    if existing_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id {movie_id} does not exist")
    existing_rating: models.Ratings | None = db.query(models.Ratings).filter_by(user_id=current_user.user_id,
                                                        movie_id=movie_id).first()
    if existing_rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rating with id {current_user.user_id} has not rated movie with id {movie_id}")
    
    existing_movie.rating = UpdateRating(existing_movie.rating,
                                existing_movie.number_of_ratings,
                                existing_rating.rating,
                                rating.rating)
    existing_rating.rating = rating.rating
    db.commit()
    rating_out = schemas.RatingOutPersonal.model_validate({
        "rating": existing_rating.rating,
        "movie_id": existing_rating.movie_id,
        "title": existing_movie.title,
        "number_of_ratings": existing_movie.number_of_ratings,
        "user_id": existing_rating.user_id
    })
    return rating_out

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(
    movie_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: schemas.UserOut = Depends(get_current_user_auth)
):
    
    existing_movie: models.Movies | None = db.query(models.Movies).filter_by(movie_id=movie_id).first()
    if existing_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id {movie_id} does not exist")
    existing_rating: models.Ratings | None = db.query(models.Ratings).filter_by(user_id=current_user.user_id,
                                                        movie_id=movie_id).first()
    if existing_rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rating with id {current_user.user_id} has not rated movie with id {movie_id}")
    
    db.delete(existing_rating)
    existing_movie.rating = RemoveRating(existing_movie.rating,
                                         existing_movie.number_of_ratings,
                                         existing_rating.rating)
    existing_movie.number_of_ratings -= 1
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)