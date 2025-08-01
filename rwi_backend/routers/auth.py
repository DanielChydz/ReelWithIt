from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from rwi_backend import schemas
from sqlalchemy.orm import Session
from rwi_backend.database import get_db
from rwi_backend.oauth2 import create_access_token, create_refresh_token, verify_access_token
from rwi_backend.utils import HashPassword, VerifyPassword
from rwi_backend.models import Users
from rwi_backend.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Create user
@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate,
    db: Annotated[Session, Depends(get_db)]
) -> schemas.UserOut:
    
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
@router.post("/login", response_model=schemas.Token)
def login_user(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
    response: Response
) -> schemas.Token:
    
    user: Users | None = db.query(Users).filter(Users.email == user_credentials.username).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    if not VerifyPassword(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    time_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: schemas.Token = create_access_token({"id": user.user_id}, time_delta)
    time_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token: schemas.Token = create_refresh_token({"id": user.user_id}, time_delta)
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token.token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        max_age=7*24*60*60
    )
    
    return access_token

# Refresh token
@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    request: Request,
    response: Response
):
    
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_id: schemas.TokenData = verify_access_token(refresh_token)
    time_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    new_refresh_token = create_access_token({"id": user_id.user_id}, time_delta)
    
    return new_refresh_token