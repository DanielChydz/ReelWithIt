from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import SecretStr
from sqlalchemy import or_
from rwi_backend import models, schemas
from sqlalchemy.orm import Session
from rwi_backend.database import get_db
from rwi_backend.utils import HashPassword
from rwi_backend.oauth2 import oauth2_scheme, get_current_user

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

# Read user
@router.get("/{username}", response_model=schemas.UserOut)
def get_user(
    username: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: schemas.UserOut = Depends(get_current_user)
) -> schemas.UserOut:
    
    # Check if user exists
    existing_user = db.query(models.Users).filter(models.Users.username == username).first()
    if existing_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")
    user_model_to_schema = schemas.UserOut.model_validate(existing_user)
    return user_model_to_schema

# Update user
@router.put("/{username}", response_model=schemas.UserOut)
def update_user(
    username: str,
    user: schemas.UserCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: schemas.UserOut = Depends(get_current_user)
) -> schemas.UserOut:
    
    existing_user: models.Users | None = db.query(models.Users).filter(models.Users.username == username).first()
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")
    if username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User {current_user.username} has no permission to update user {username}")
    
    existing_data: models.Users | None = db.query(models.Users).filter(or_(models.Users.username == user.username, models.Users.email == user.email), models.Users.user_id != existing_user.user_id).first()
    if existing_data:
        if existing_data.email == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Can't change email to {user.email} - already taken")
        if existing_data.username == user.username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Can't change username to {user.username} - already taken")
        
    updated_user = existing_user
    updated_user.password = HashPassword(user.password)
    updated_user.username = user.username
    updated_user.email = user.email
    
    db.commit()
    db.refresh(updated_user)
    
    return schemas.UserOut.model_validate(updated_user)

# Delete user
@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    username: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: schemas.UserOut = Depends(get_current_user)
):
    
    existing_user = db.query(models.Users).filter(models.Users.username == username).first()
    if existing_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")
    if username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete another user")
    
    db.delete(existing_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)