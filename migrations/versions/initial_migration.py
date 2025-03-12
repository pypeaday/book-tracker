"""Initial migration

Revision ID: initial_migration
Create Date: 2025-03-12 17:11

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create book_status enum type
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=True),
        sa.Column('status', sa.Enum('to_read', 'reading', 'completed', 'on_hold', 'dnf', name='book_status'), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('completion_date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_id'), 'books', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_books_id'), table_name='books')
    op.drop_table('books')
