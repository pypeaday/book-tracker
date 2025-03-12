"""Add rating field

Revision ID: add_rating_field
Create Date: 2025-03-12 17:14
Revises: initial_migration

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_rating_field'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('books', sa.Column('rating', sa.SmallInteger(), nullable=True, 
                                   comment='0: DNF, 1: Wouldn\'t read again, 2: Good but not recommendable, 3: Would recommend'))

def downgrade() -> None:
    op.drop_column('books', 'rating')
