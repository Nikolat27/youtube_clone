"""I changed videos field to video

Revision ID: cec64a858bc2
Revises: 9acc5244fc0e
Create Date: 2025-01-19 18:30:51.555987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cec64a858bc2'
down_revision: Union[str, None] = '9acc5244fc0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('histories')


def downgrade() -> None:
    op.create_table('histories',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('video_id', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='histories_user_id_fkey'),
    sa.ForeignKeyConstraint(['video_id'], ['videos.unique_id'], name='histories_video_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='histories_pkey')
    )
