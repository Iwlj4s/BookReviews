"""add rating field to deletedreview model

Revision ID: aef69353cb0e
Revises: bd9ff687e3bb
Create Date: 2025-05-04 11:17:34.639071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aef69353cb0e'
down_revision: Union[str, None] = 'bd9ff687e3bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Adding new columns to the reviews table
    # op.add_column('deleted_reviews', sa.Column('rating', sa.Integer(), nullable=True))
    pass


def downgrade():
    # Dropping the columns if we need to rollback
    # op.drop_column('deleted_reviews', 'rating')
    pass
