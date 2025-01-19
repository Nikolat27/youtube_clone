"""Hi

Revision ID: 873f5e990ce9
Revises: 6251725dba76
Create Date: 2025-01-19 18:36:08.506312

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "873f5e990ce9"
down_revision: Union[str, None] = "6251725dba76"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the new table with the updated schema
    op.create_table(
        "histories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("views", sa.String(length=30), nullable=False),  # Updated field name
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="histories_user_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["views"], ["videos.unique_id"], name="histories_views_fkey"
        ),  # Updated field name
        sa.PrimaryKeyConstraint("id", name="histories_pkey"),
    )


def downgrade() -> None:
    op.drop_table("histories")
