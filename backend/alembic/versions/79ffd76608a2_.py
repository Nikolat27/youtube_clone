"""empty message

Revision ID: 79ffd76608a2
Revises: 924638e03afc
Create Date: 2024-12-28 02:49:19.504106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79ffd76608a2'
down_revision: Union[str, None] = '924638e03afc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('communities',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('community_text', sa.String(length=200), nullable=False),
    sa.Column('image_name', sa.String(length=200), nullable=True),
    sa.Column('image_url', sa.String(length=400), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('communities')
    # ### end Alembic commands ###