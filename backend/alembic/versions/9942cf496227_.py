"""empty message

Revision ID: 9942cf496227
Revises: 43c1d04a04d7
Create Date: 2025-01-19 01:08:43.886753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9942cf496227'
down_revision: Union[str, None] = '43c1d04a04d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
