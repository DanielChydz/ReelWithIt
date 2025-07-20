"""Changed email column and fkey to id

Revision ID: 46f24795479c
Revises: 2034278cf859
Create Date: 2025-06-22 22:00:43.476327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46f24795479c'
down_revision: Union[str, None] = '2034278cf859'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # drop old constraints
    op.drop_constraint("ratings_pkey", "ratings", type_="primary")
    op.drop_constraint("ratings_email_fkey", "ratings", type_="foreignkey")
    
    # drop old column
    op.drop_column("ratings", "email")
    
    # add new column
    op.add_column("ratings", sa.Column("user_id", sa.Integer(), nullable=False))
    
    # add primary key
    op.create_primary_key(
        constraint_name=None,
        table_name="ratings",
        columns=["user_id", "movie_id"]
    )
    
    # add foreign keys
    op.create_foreign_key(
        constraint_name=None,
        source_table="ratings",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )
    op.create_foreign_key(
        constraint_name=None,
        source_table="ratings",
        referent_table="movies",
        local_cols=["movie_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )

def downgrade() -> None:
    # drop pkey and fkey
    op.drop_constraint("pk_ratings", "ratings", type_="primary")
    op.drop_constraint("fk_ratings_user_id_users", "ratings", type_="foreignkey")
    op.drop_constraint("fk_ratings_movie_id_movies", "ratings", type_="foreignkey")

    # delete user_id
    op.drop_column("ratings", "user_id")

    # bring back email column
    op.add_column("ratings", sa.Column("email", sa.String(), nullable=False))

    # bring back fkey
    op.create_foreign_key(
        constraint_name="ratings_email_fkey",
        source_table="ratings",
        referent_table="users",
        local_cols=["email"],
        remote_cols=["email"],
        ondelete="CASCADE"
    )

    # bring back pkey
    op.create_primary_key("ratings_pkey", "ratings", ["email", "movie_id"])