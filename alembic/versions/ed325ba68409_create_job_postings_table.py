"""create job_postings table

Revision ID: ed325ba68409
Revises: 21c02eef3fb8
Create Date: 2026-10-21 09:33:04.940457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed325ba68409'
down_revision: Union[str, Sequence[str], None] = '21c02eef3fb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to create job_postings table."""
    op.create_table(
        'job_postings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('company', sa.String(length=255), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('job_type', sa.String(length=50), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('requirements', sa.Text(), nullable=True),
        sa.Column('salary_range', sa.String(length=100), nullable=True),
        sa.Column('application_deadline', sa.String(length=20), nullable=True),
        sa.Column('contact_email', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.String(length=20), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('job_postings', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_job_postings_id'), ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema to drop job_postings table."""
    with op.batch_alter_table('job_postings', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_job_postings_id'))

    op.drop_table('job_postings')
