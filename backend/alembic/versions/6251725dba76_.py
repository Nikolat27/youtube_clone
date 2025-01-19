"""empty message

Revision ID: 6251725dba76
Revises: cec64a858bc2
Create Date: 2025-01-19 18:33:39.185861

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6251725dba76"
down_revision: Union[str, None] = "cec64a858bc2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
    op.create_table(
        "histories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "video_id", sa.String(length=30), nullable=False
        ),  # Original field name
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="histories_user_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["video_id"], ["videos.unique_id"], name="histories_video_id_fkey"
        ),  # Original field name
        sa.PrimaryKeyConstraint("id", name="histories_pkey"),
    )
