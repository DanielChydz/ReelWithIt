from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from rwi_backend import models
from rwi_backend import schemas
from rwi_backend.database import get_db
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(hash_data: dict, expires_delta: timedelta = timedelta(minutes=5)) -> schemas.Token:
    to_encode = hash_data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ENCODING_ALGORITHM)
    token: schemas.Token = schemas.Token(access_token=encoded_jwt)
    return token

def verify_access_token(token: str) -> schemas.TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, [settings.ENCODING_ALGORITHM])
        id: int | None = payload.get("id")
        if id is None:
            raise credentials_exception
        return schemas.TokenData(user_id=id)
    except JWTError:
        raise credentials_exception

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]) -> schemas.UserOut:
    user_token_data: schemas.TokenData = verify_access_token(token)
    user: models.Users | None = db.query(models.Users).filter(models.Users.user_id == user_token_data.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_token_data.user_id} not found - account banned, removed or never existed")
    return schemas.UserOut.model_validate(user)