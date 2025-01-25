"""empty message

Revision ID: 71e0eedfe7bd
Revises: 97aab5427256
Create Date: 2025-01-25 15:21:46.908551

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "71e0eedfe7bd"
down_revision: Union[str, None] = "97aab5427256"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ads",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "unique_id",
            sa.VARCHAR(length=80),
            autoincrement=False,
            nullable=False,
            unique=True,
        ),
        sa.Column("title", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column(
            "company_contact_url",
            sa.VARCHAR(length=100),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "company_picture_url",
            sa.VARCHAR(length=100),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "file_url", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="ads_pkey"),
        sa.UniqueConstraint("unique_id", name="ads_unique_id_key"),
    )


def downgrade() -> None:
    pass
