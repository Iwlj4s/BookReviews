"""Fix reviews id autoincrement and foreign keys

Revision ID: b30c2313b02e
Revises: aef69353cb0e
Create Date: 2025-05-21 10:07:45.417437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b30c2313b02e'
down_revision: Union[str, None] = 'aef69353cb0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Удаляем обзоры с некорректным id
    op.execute("DELETE FROM reviews WHERE id = 0")

    # 2. Переименовываем старую таблицу
    op.rename_table('reviews', 'reviews_old')

    # 3. Создаём новую таблицу reviews с правильной структурой
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('reviewed_book_id', sa.Integer, sa.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
        sa.Column('reviewed_book_author_id', sa.Integer, sa.ForeignKey('authors.id', ondelete='CASCADE'), nullable=False),
        sa.Column('reviewed_book_cover', sa.String, nullable=False),
        sa.Column('rating', sa.Integer),
        sa.Column('review_title', sa.String),
        sa.Column('review_body', sa.Text, nullable=False),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('updated', sa.DateTime, nullable=False),
    )

    # 4. Копируем данные из старой таблицы (только с id > 0)
    op.execute("""
        INSERT INTO reviews (
            id, created_by, reviewed_book_id, reviewed_book_author_id, reviewed_book_cover, rating, review_title, review_body, created, updated
        )
        SELECT
            id, created_by, reviewed_book_id, reviewed_book_author_id, reviewed_book_cover, rating, review_title, review_body, created, updated
        FROM reviews_old
        WHERE id > 0
    """)

    # 5. Удаляем старую таблицу
    op.drop_table('reviews_old')

def downgrade():
    # Откатить миграцию можно аналогично, если нужно
    pass