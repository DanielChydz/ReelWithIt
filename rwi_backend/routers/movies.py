from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from rwi_backend import models, schemas
from rwi_backend.database import get_db
from rwi_backend.oauth2 import get_current_user

router = APIRouter(
    prefix="/movie",
    tags=["movies"]
)

# frontend debugging, remove later
@router.get("/all", response_model=list[schemas.MovieOut])
def get_movies(
    db: Annotated[Session, Depends(get_db)],
) -> list[schemas.MovieOut]:
    movies = db.query(models.Movies).all()
    return [schemas.MovieOut.model_validate(m) for m in movies]

# Create movie
@router.post("/", response_model=schemas.MovieOut, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie: schemas.MovieCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: schemas.UserOut = Depends(get_current_user)
) -> schemas.MovieOut:
    existing_movie = db.query(models.Movies).filter(
        models.Movies.title == movie.title,
        models.Movies.year == movie.year,
        models.Movies.director == movie.director
    ).first()
    
    if existing_movie:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Movie already exists")
    
    new_movie = models.Movies(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return schemas.MovieOut.model_validate(new_movie)

# Read movie
@router.get("/{id}", response_model=schemas.MovieOut)
def get_movie(
    id: int,
    db: Annotated[Session, Depends(get_db)],
) -> schemas.MovieOut:
    # Check if movie exists
    existing_movie = db.query(models.Movies).filter(models.Movies.movie_id == id).first()
    if existing_movie == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id {id} not found")
         
    return schemas.MovieOut.model_validate(existing_movie)

# Update movie
@router.put("/{id}", response_model=schemas.MovieOut)
def update_movie(
    id: int,
    movie: schemas.MovieCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: schemas.UserOut = Depends(get_current_user)
) -> schemas.MovieOut:
    # Check if movie exists
    existing_movie = db.query(models.Movies).filter(models.Movies.movie_id == id).first()
    if existing_movie == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id {id} not found")
    if schemas.MovieCreate.model_validate(existing_movie) == movie:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Movie {movie.title} ({movie.year}, {movie.year}) already exists")
    
    existing_movie.title = movie.title
    existing_movie.year = movie.year
    existing_movie.director = movie.director
    
    return schemas.MovieOut.model_validate(existing_movie)

# Delete movie
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: schemas.UserOut = Depends(get_current_user)
):
    # Check if movie exists
    existing_movie = db.query(models.Movies).filter(models.Movies.movie_id == id).first()
    if existing_movie == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id {id} not found")
    
    db.delete(existing_movie)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)