"""add index on token_blacklist.token

Revision ID: c1d2e3f4a5b6
Revises: b2c3d4e5f6a7
Create Date: 2026-05-11
"""
from alembic import op

revision = 'c1d2e3f4a5b6'
down_revision = '319d2bfc4918'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_token_blacklist_token", "token_blacklist", ["token"])


def downgrade() -> None:
    op.drop_index("ix_token_blacklist_token", table_name="token_blacklist")
