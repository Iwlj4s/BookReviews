"""add bio to user

Revision ID: 66dc13052226
Revises: d0fcc9c66abb
Create Date: 2025-04-19 10:53:42.595654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66dc13052226'
down_revision: Union[str, None] = 'd0fcc9c66abb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('bio', sa.String(), nullable=True, server_default='No bio'))


def downgrade() -> None:
    op.drop_column('users', 'bio')

