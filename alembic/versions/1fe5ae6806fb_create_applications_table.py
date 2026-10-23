"""create applications table

Revision ID: 1fe5ae6806fb
Revises: ed325ba68409
Create Date: 2026-10-21 10:44:10.093294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fe5ae6806fb'
down_revision: Union[str, Sequence[str], None] = 'ed325ba68409'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to create applications table."""
    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('resume_url', sa.String(length=500), nullable=True),
        sa.Column('cover_note', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='Pending'),
        sa.Column('created_at', sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(['job_id'], ['job_postings.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_applications_id'), ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema to drop applications table."""
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_applications_id'))

    op.drop_table('applications')

