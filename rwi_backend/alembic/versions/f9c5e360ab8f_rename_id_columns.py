"""rename id columns

Revision ID: f9c5e360ab8f
Revises: 46f24795479c
Create Date: 2025-06-28 04:36:39.010242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9c5e360ab8f'
down_revision: Union[str, None] = '46f24795479c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # drop fkeys
    op.drop_constraint("fk_ratings_user_id_users", "ratings", type_="foreignkey")
    op.drop_constraint("fk_ratings_movie_id_movies", "ratings", type_="foreignkey")

    # change column name
    op.alter_column("users", "id", new_column_name="user_id")
    op.alter_column("movies", "id", new_column_name="movie_id")

    # recreate fkeys
    op.create_foreign_key(
        None,
        "ratings", "users",
        ["user_id"], ["user_id"],
        ondelete="CASCADE"
    )
    op.create_foreign_key(
        None,
        "ratings", "movies",
        ["movie_id"], ["movie_id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("fk_ratings_user_id_users", "ratings", type_="foreignkey")
    op.drop_constraint("fk_ratings_movie_id_movies", "ratings", type_="foreignkey")

    op.alter_column("users", "user_id", new_column_name="id")
    op.alter_column("movies", "movie_id", new_column_name="id")

    op.create_foreign_key(
        "fk_ratings_user_id_users",
        "ratings", "users",
        ["user_id"], ["id"],
        ondelete="CASCADE"
    )
    op.create_foreign_key(
        "fk_ratings_movie_id_movies",
        "ratings", "movies",
        ["movie_id"], ["id"],
        ondelete="CASCADE"
    )

