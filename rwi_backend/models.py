from datetime import datetime
from .database import Base
from sqlalchemy import TIMESTAMP, CheckConstraint, Column, Float, Integer, Numeric, String, text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Users(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    
    ratings = relationship("Ratings", back_populates="users")
    
    __table_args__ = (
        CheckConstraint("user_id >= 0", name="id_non_negative"),
    )
    
class Movies(Base):
    __tablename__ = "movies"
    
    movie_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False, server_default=text("5"))
    number_of_ratings: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    director: Mapped[str] = mapped_column(String(64), nullable=False)
    
    __table_args__ = (
        CheckConstraint("movie_id >= 0", name="id_non_negative"),
        CheckConstraint("rating >= 1 AND rating <=10", name="rating_in_range"),
        CheckConstraint("year >= 1800 AND year <= 2100", name="year_in_range"),
    )

    ratings = relationship("Ratings", back_populates="movies")

class Ratings(Base):
    __tablename__ = "ratings"
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), primary_key=True)
    rating: Mapped[float] = mapped_column(Numeric(3, 1), nullable=False)
    
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 10", name="rating_in_range"),
    )
    
    users = relationship("Users", back_populates="ratings")
    movies = relationship("Movies", back_populates="ratings")