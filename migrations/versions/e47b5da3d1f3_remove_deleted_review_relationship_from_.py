"""Remove deleted_review relationship from Review

Revision ID: e47b5da3d1f3
Revises: b30c2313b02e
Create Date: 2025-06-03 14:26:35.789415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e47b5da3d1f3'
down_revision: Union[str, None] = 'b30c2313b02e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Удаляем внешний ключ review_id из deleted_reviews
    with op.batch_alter_table('deleted_reviews') as batch_op:
        batch_op.drop_constraint('deleted_reviews_review_id_fkey', type_='foreignkey')
        batch_op.drop_column('review_id')


def downgrade():
    with op.batch_alter_table('deleted_reviews') as batch_op:
        batch_op.add_column(sa.Column('review_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('deleted_reviews_review_id_fkey', 'reviews', ['review_id'], ['id'])
