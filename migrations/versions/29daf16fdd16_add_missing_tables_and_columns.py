"""add missing tables and columns

Revision ID: 29daf16fdd16
Revises: 66dc13052226
Create Date: 2025-04-24 14:34:07.112365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29daf16fdd16'
down_revision: Union[str, None] = '66dc13052226'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add new columns to User table
    op.add_column('users', sa.Column('profile_picture', sa.String(), nullable=True))
    op.add_column('users', sa.Column('registration_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default=sa.text('1')))

    # Add new column to Author table
    op.add_column('authors', sa.Column('biography', sa.Text(), nullable=True))

    # Add new columns to Book table
    op.add_column('books', sa.Column('average_rating', sa.Float(), nullable=True))
    op.add_column('books', sa.Column('publication_year', sa.Integer(), nullable=True))

    # Create AdminAction table
    op.create_table('admin_actions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('action_type', sa.String(), nullable=False),
        sa.Column('action_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('target_user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('performed_by_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create BookRating table
    op.create_table('book_ratings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('book_id', sa.Integer(), sa.ForeignKey('books.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create ExternalRating table
    op.create_table('external_ratings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('external_rating', sa.Float(), nullable=False),
        sa.Column('external_url', sa.String(), nullable=True),
        sa.Column('book_id', sa.Integer(), sa.ForeignKey('books.id'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Warning table
    op.create_table('warnings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('expiration_date', sa.DateTime(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('0')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('admin_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create BlockedUser table
    op.create_table('blocked_users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('block_start', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('block_end', sa.DateTime(), nullable=True),
        sa.Column('is_permanent', sa.Boolean(), server_default=sa.text('0')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('admin_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create DeletedReview table
    op.create_table('deleted_reviews',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('deletion_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('original_content', sa.Text(), nullable=False),
        sa.Column('review_id', sa.Integer(), sa.ForeignKey('reviews.id'), nullable=False),
        sa.Column('admin_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Add is_deleted column to Review table
    op.add_column('reviews', sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('0')))


def downgrade():
    # Drop all new tables
    op.drop_table('deleted_reviews')
    op.drop_table('blocked_users')
    op.drop_table('warnings')
    op.drop_table('external_ratings')
    op.drop_table('book_ratings')
    op.drop_table('admin_actions')

    # Drop new columns from Book table
    op.drop_column('books', 'publication_year')
    op.drop_column('books', 'average_rating')

    # Drop new column from Author table
    op.drop_column('authors', 'biography')

    # Drop new columns from User table
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'registration_date')
    op.drop_column('users', 'profile_picture')

    # Drop is_deleted column from Review table
    op.drop_column('reviews', 'is_deleted')