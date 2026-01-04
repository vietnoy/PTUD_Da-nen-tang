"""Add is_active to foods

Revision ID: b5c7a5cf6c3c
Revises: d1a499f2ff3e
Create Date: 2026-01-04 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b5c7a5cf6c3c"
down_revision = "d1a499f2ff3e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ensure foods.is_active exists for soft deletes and filtering
    op.execute(
        "ALTER TABLE foods ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE"
    )
    # Backfill any nulls in case the column existed without a default
    op.execute("UPDATE foods SET is_active = TRUE WHERE is_active IS NULL")


def downgrade() -> None:
    op.drop_column("foods", "is_active")
