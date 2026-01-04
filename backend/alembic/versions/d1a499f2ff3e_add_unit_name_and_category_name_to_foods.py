"""add_unit_name_and_category_name_to_foods

Revision ID: d1a499f2ff3e
Revises: 26a9a495ec51
Create Date: 2026-01-04 01:52:28.380337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1a499f2ff3e'
down_revision = '26a9a495ec51'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add unit_name and category_name columns to foods table
    op.add_column('foods', sa.Column('unit_name', sa.String(length=20), nullable=True))
    op.add_column('foods', sa.Column('category_name', sa.String(length=50), nullable=True))


def downgrade() -> None:
    # Remove unit_name and category_name columns from foods table
    op.drop_column('foods', 'category_name')
    op.drop_column('foods', 'unit_name')