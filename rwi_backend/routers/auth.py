from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from rwi_backend import schemas
from sqlalchemy.orm import Session
from rwi_backend.database import get_db
from rwi_backend.oauth2 import create_access_token
from rwi_backend.utils import HashPassword, VerifyPassword
from rwi_backend.models import Users
from rwi_backend.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Create user
@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]) -> schemas.UserOut:
    # Check if user exists
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with e-mail {user.email} already exists.")
    existing_user = db.query(Users).filter(Users.username == user.username).first()
    if existing_user != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with username {user.username} already exists.")
    
    hashedPwd = HashPassword(user.password)
    new_user = Users(**user.model_dump(exclude={"password"}), password=hashedPwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    new_user_out = schemas.UserOut.model_validate(new_user)
    return new_user_out
    
# Login user
@router.post("/login", response_model=schemas.UserWithTokenOut)
def login_user(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]) -> schemas.UserWithTokenOut:
    user: Users | None = db.query(Users).filter(Users.email == user_credentials.username).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    if not VerifyPassword(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    time_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: schemas.Token = create_access_token({"id": user.user_id}, time_delta)
    user_with_token_out = schemas.UserWithTokenOut(
        access_token=access_token.access_token,
        token_type=access_token.token_type,
        user=schemas.UserOut.model_validate(user)
    )
    return user_with_token_out