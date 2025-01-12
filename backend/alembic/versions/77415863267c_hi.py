"""hi

Revision ID: 77415863267c
Revises: 3ca37cf8e019
Create Date: 2025-01-12 23:57:45.941396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '77415863267c'
down_revision: Union[str, None] = '3ca37cf8e019'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('communities')
    op.drop_table('community_likes')

def downgrade() -> None:
    op.create_table('communities',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('community_text', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('image_name', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('image_url', sa.VARCHAR(length=400), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='communities_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='communities_pkey')
    )