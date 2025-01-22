"""I added ondelete cascade to history

Revision ID: 97aab5427256
Revises: 452ad560b7fd
Create Date: 2025-01-23 00:13:55.589797

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "97aab5427256"
down_revision: Union[str, None] = "452ad560b7fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("histories_video_id_fkey", "histories", type_="foreignkey")
    op.create_foreign_key(
        "histories_video_id_fkey",
        "histories",
        "videos",
        ["video_id"],
        ["unique_id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    pass
