"""added exprire column to RefreshSession as datetime

Revision ID: 0f105a40349a
Revises: 77f5ff776ec4
Create Date: 2023-07-21 21:56:30.369576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f105a40349a'
down_revision = '77f5ff776ec4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('refresh_sessions', sa.Column('expire', sa.DateTime(timezone=True), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('refresh_sessions', 'expire')
    # ### end Alembic commands ###
