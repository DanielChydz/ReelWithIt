from typing import Generator
from fastapi.testclient import TestClient
from fastapi import status
from httpx import Response
from pydantic import SecretStr
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from rwi_backend.main import rwi
from rwi_backend.config import settings
from rwi_backend.database import get_db, Base
from rwi_backend.oauth2 import create_access_token
from rwi_backend import models, schemas
from rwi_backend.utils import HashPassword

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PWD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}_devtest"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"connect_timeout": 3})

TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def session() -> Generator[Session, None, None]:
    engine.dispose()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db: Session = TestingSessionLocal()
    
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    rwi.dependency_overrides[get_db] = override_get_db
    
    try:
        yield db
    finally:
        db.close()
        rwi.dependency_overrides.clear()

@pytest.fixture
def test_user(session: Session) -> schemas.UserOut:
    user_data = {
        "email": "testemail@domain.com",
        "username": "testusername",
        "password": HashPassword(SecretStr("testpassword"))
    }
    user = models.Users(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return schemas.UserOut.model_validate(user)

@pytest.fixture
def test_user_token(test_user: schemas.UserOut, session: Session) -> schemas.Token:
    user: models.Users | None = session.query(models.Users).filter(models.Users.username == test_user.username).first()
    assert user is not None
    return create_access_token({"id": user.user_id})

@pytest.fixture
def unauthorized_client() -> Generator[TestClient, None, None]:
    yield TestClient(rwi)

@pytest.fixture
def authorized_client(test_user_token: schemas.Token) -> TestClient:
    authorized_client = TestClient(rwi)
    authorized_client.headers = {**authorized_client.headers, "Authorization": f"Bearer {test_user_token.token}"}
    return authorized_client

@pytest.fixture
def test_movie(
    authorized_client: TestClient
) -> schemas.MovieOut:
    new_movie = {"title": "title", "year": 2000, "director": "director"}
    rwi_response: Response = authorized_client.post("/movie", json=new_movie)
    assert rwi_response.status_code == status.HTTP_201_CREATED
    return schemas.MovieOut.model_validate(rwi_response.json())

@pytest.fixture(scope="session", autouse=True)
def clear_db_override():
    yield