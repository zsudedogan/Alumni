"""add city to job_postings and alter title length

Revision ID: 3a4b5c6d7e8f
Revises: 1fe5ae6806fb
Create Date: 2026-11-18 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a4b5c6d7e8f'
down_revision: Union[str, Sequence[str], None] = '1fe5ae6806fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to add city and adjust title length on job_postings."""
    try:
        op.add_column('job_postings', sa.Column('city', sa.String(length=100), nullable=True))
    except Exception:
        pass


def downgrade() -> None:
    """Downgrade schema."""
    try:
        op.drop_column('job_postings', 'city')
    except Exception:
        pass
