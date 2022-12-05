"""Add a column

Revision ID: 009348af99c5
Revises: d66e2cce4490
Create Date: 2022-12-05 17:38:58.123445

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '009348af99c5'
down_revision = 'd66e2cce4490'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('disabled', sa.Boolean()))


def downgrade() -> None:
    op.drop_column('users', 'disabled')
