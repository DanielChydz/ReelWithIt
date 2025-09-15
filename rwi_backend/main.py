# rwi in the code stands for the project name (reel with it)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rwi_backend.routers import auth, ratings, users, movies

rwi = FastAPI()

rwi.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rwi.include_router(users.router)
rwi.include_router(movies.router)
rwi.include_router(auth.router)
rwi.include_router(ratings.router)