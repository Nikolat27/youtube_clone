"""Sam

Revision ID: 15b0a42a3d19
Revises: 76c01ae33f61
Create Date: 2025-01-19 22:55:57.565800

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "15b0a42a3d19"
down_revision: Union[str, None] = "76c01ae33f61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the new column `watch_history_enable` to the `users` table
    op.alter_column(
        "users",
        sa.Column(
            "watch_history_enable",
            sa.Boolean(),
            server_default="true",  # Default value for existing rows
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "watch_history_enable")
