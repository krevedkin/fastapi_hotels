"""added exprire column to RefreshSessions

Revision ID: d4c1e707b91a
Revises: cf6611f30523
Create Date: 2023-07-21 03:23:08.275073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4c1e707b91a'
down_revision = 'cf6611f30523'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('refresh_sessions', sa.Column('expire', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('refresh_sessions', 'expire')
    # ### end Alembic commands ###
