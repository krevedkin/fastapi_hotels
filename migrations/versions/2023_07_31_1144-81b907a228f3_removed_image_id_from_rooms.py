"""Removed image_id from Rooms

Revision ID: 81b907a228f3
Revises: ba4c6022ec26
Create Date: 2023-07-31 11:44:09.579228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81b907a228f3'
down_revision = 'ba4c6022ec26'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rooms', 'image_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
