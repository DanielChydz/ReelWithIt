from pydantic import AwareDatetime, BaseModel, ConfigDict, EmailStr, Field, SecretStr, StringConstraints, field_validator
from typing import Annotated, Literal

class UserCreate(BaseModel):
    email: Annotated[EmailStr, StringConstraints(min_length=5, max_length=254)]
    username: Annotated[str, StringConstraints(min_length=1, max_length=32)]
    password: Annotated[SecretStr, StringConstraints(min_length=6, max_length=32)]

class UserOut(BaseModel):
    user_id: Annotated[int, Field(strict=True, ge=0)]
    email: Annotated[EmailStr, StringConstraints(min_length=5, max_length=254)]
    username: Annotated[str, StringConstraints(min_length=1, max_length=32)]
    created_at: AwareDatetime
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: Literal["Bearer"] = "Bearer"

class UserWithTokenOut(Token):
    user: UserOut

class TokenData(BaseModel):
    user_id: int

class MovieCreate(BaseModel):
    title: Annotated[str, StringConstraints(min_length=1, max_length=64)]
    year: Annotated[int, Field(strict=True, ge=1800, le=2100)]
    director: Annotated[str, StringConstraints(min_length=1, max_length=64)]
    
    model_config = ConfigDict(from_attributes=True)
    
class MovieOut(MovieCreate):
    movie_id: Annotated[int, Field(strict=True, gt=0)]
    
    model_config = ConfigDict(from_attributes=True)
    
class RatingAdd(BaseModel):
    rating: Annotated[float, Field(strict=True, ge=1, le=10)]
    
    @field_validator("rating")
    def one_decimal_place(cls, val):
        if round(val,  1) != val:
            raise ValueError("Rating must have only one decimal place")
        return val
    
    model_config = ConfigDict(from_attributes=True)
    
class RatingOut(RatingAdd):
    movie_id: Annotated[int, Field(strict=True, gt=0)]
    title: Annotated[str, StringConstraints(min_length=1, max_length=64)]
    number_of_ratings: Annotated[int, Field(strict=True, ge=0)]
    
    model_config = ConfigDict(from_attributes=True)

class RatingOutPersonal(RatingOut):
    user_id: Annotated[int, Field(strict=True, gt=0)]
    
    model_config = ConfigDict(from_attributes=True)