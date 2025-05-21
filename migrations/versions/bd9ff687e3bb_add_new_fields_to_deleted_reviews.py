"""add_new_fields_to_deleted_reviews

Revision ID: bd9ff687e3bb
Revises: 
Create Date: 2025-05-04 11:04:18.457317

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd9ff687e3bb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # SQLite требует особого подхода к добавлению NOT NULL колонок в существующую таблицу
    # with op.batch_alter_table('deleted_reviews') as batch_op:
    #     #batch_op.add_column(sa.Column('reason', sa.String(), nullable=True))
    #     batch_op.add_column(sa.Column('book_id', sa.Integer(), nullable=False, server_default='0'))
    #     batch_op.add_column(sa.Column('book_name', sa.String(), nullable=False, server_default=''))
    #     batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=False, server_default='0'))
    #     batch_op.add_column(sa.Column('author_name', sa.String(), nullable=False, server_default=''))
    #     batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False, server_default='0'))
    #     batch_op.add_column(sa.Column('user_name', sa.String(), nullable=False, server_default=''))
    #
    # # Для SQLite внешние ключи нужно включить отдельно
    # op.execute('PRAGMA foreign_keys=ON')
    #
    # # Создаем foreign key constraints (SQLite поддерживает их, но с ограничениями)
    # with op.batch_alter_table('deleted_reviews') as batch_op:
    #     batch_op.create_foreign_key(
    #         'fk_deleted_reviews_book_id',
    #         'books', ['book_id'], ['id']
    #     )
    #     batch_op.create_foreign_key(
    #         'fk_deleted_reviews_author_id',
    #         'authors', ['author_id'], ['id']
    #     )
    #     batch_op.create_foreign_key(
    #         'fk_deleted_reviews_user_id',
    #         'users', ['user_id'], ['id']
    #     )
    pass


def downgrade():
    # # Удаляем foreign key constraints
    # with op.batch_alter_table('deleted_reviews') as batch_op:
    #     batch_op.drop_constraint('fk_deleted_reviews_user_id', type_='foreignkey')
    #     batch_op.drop_constraint('fk_deleted_reviews_author_id', type_='foreignkey')
    #     batch_op.drop_constraint('fk_deleted_reviews_book_id', type_='foreignkey')
    #
    # # Удаляем колонки
    # with op.batch_alter_table('deleted_reviews') as batch_op:
    #     batch_op.drop_column('user_name')
    #     batch_op.drop_column('user_id')
    #     batch_op.drop_column('author_name')
    #     batch_op.drop_column('author_id')
    #     batch_op.drop_column('book_name')
    #     batch_op.drop_column('book_id')
    #     batch_op.drop_column('reason')
    pass