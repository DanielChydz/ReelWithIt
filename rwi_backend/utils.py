from pydantic import SecretStr
from passlib.context import CryptContext

password_hash = CryptContext(schemes=["argon2"], deprecated="auto")

def HashPassword(pwd: SecretStr) -> str:
    return password_hash.hash(pwd.get_secret_value())

def VerifyPassword(plain_password, hashed_password) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def AddRating(
    current_rating: float,
    current_number_of_ratings: int,
    added_rating: float
) -> float:
    
    if (round(added_rating, 1) != added_rating) or (added_rating < 1) or (added_rating > 10):
        raise ValueError("Invalid rating")
    if current_number_of_ratings == 0:
        return added_rating
    new_rating: float = (current_rating * current_number_of_ratings + added_rating) / (current_number_of_ratings + 1)
    return new_rating

def RemoveRating(
    current_rating: float,
    current_number_of_ratings: int,
    removed_rating: float
) -> float:
    
    if current_number_of_ratings == 1:
        return 5
    new_rating: float = (current_rating * current_number_of_ratings - removed_rating) / (current_number_of_ratings - 1)
    return new_rating

def UpdateRating(
    current_rating: float,
    current_number_of_ratings: int,
    old_rating: float,
    new_rating: float
) -> float:
    
    if (round(new_rating, 1) != new_rating) or (new_rating < 1) or (new_rating > 10):
        raise ValueError("Invalid rating")
    removed_old_rating = RemoveRating(current_rating, current_number_of_ratings, old_rating)
    added_new_rating = AddRating(removed_old_rating, current_number_of_ratings, new_rating)
    return added_new_rating