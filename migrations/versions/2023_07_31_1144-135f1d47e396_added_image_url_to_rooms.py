"""Added image_url to Rooms

Revision ID: 135f1d47e396
Revises: 81b907a228f3
Create Date: 2023-07-31 11:44:34.786963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '135f1d47e396'
down_revision = '81b907a228f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('image_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rooms', 'image_url')
    # ### end Alembic commands ###
