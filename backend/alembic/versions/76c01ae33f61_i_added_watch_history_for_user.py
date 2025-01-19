"""I added watch history for user

Revision ID: 76c01ae33f61
Revises: 8c6757ad078c
Create Date: 2025-01-19 22:45:51.040003

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "76c01ae33f61"
down_revision: Union[str, None] = "8c6757ad078c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the new column `watch_history_enable` to the `users` table
    op.add_column(
        "users",
        sa.Column(
            "watch_history_enable",
            sa.Boolean(),
            server_default="false",  # Default value for existing rows
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "watch_history_enable")
