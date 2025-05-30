from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from backend.parsing.get_data import get_book_info
from backend.src.helpers.admin_helper import check_data_for_change_author, check_data_for_change_book
from backend.src.database.database import get_db
from backend.src.database import shema, models
from backend.src.database.models import User

from backend.src.helpers import user_helper
from backend.src.helpers.general_helper import CheckHTTP404NotFound

from backend.src.DAO.general_dao import GeneralDAO
from backend.src.DAO.reviews_dao import ReviewDAO
from backend.src.DAO.users_dao import UserDAO
from backend.src.DAO.authors_dao import AuthorDAO
from backend.src.DAO.books_dao import BookDAO

from backend.src.helpers.reviews_helper import check_data_for_change_review
from backend.src.helpers.user_helper import check_data_for_change_user
from backend.src.repository.user_repository import get_current_user

from backend.email.send_email import send_email

from backend.celery.tasks import send_email_task

from backend.src.database.shema import DeletedReview as DeletedReviewSchema


# TODO: Fix getting book description
# TODO: Fix deleting review (it's putting in deleted but has some error and email doesn't sending)

async def login_admin(request: shema.UserSignIn, response, db: AsyncSession = Depends(get_db)):
    user = await user_helper.take_access_token_for_user(db=db,
                                                        response=response,
                                                        request=request,
                                                        admin_check=True)
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')


# --- USERS --- #
async def change_user(user_id: int,
                      request: shema.User,
                      admin: User = Depends(get_current_admin_user),
                      db: AsyncSession = Depends(get_db)):
    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(user_id))
    CheckHTTP404NotFound(founding_item=user, text="Пользователь не найден")

    new_data = check_data_for_change_user(request=request, user=user)

    await UserDAO.change_user(db=db,
                              user_id=user.id,
                              data=new_data)

    await db.refresh(user)

    return {
        'message': "User updated successfully",
        'status_code': 200,
        'data': {
            'id': user.id,
            'user_name': new_data.get("name"),
            'user_email': new_data.get("email")
        }
    }


async def delete_user(user_id: int,
                      admin: User = Depends(get_current_admin_user),
                      db: AsyncSession = Depends(get_db)):
    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(user_id))
    CheckHTTP404NotFound(founding_item=user, text="Пользователь не найден")

    await GeneralDAO.delete_item(db=db, item=models.User, item_id=int(user_id))
    await ReviewDAO.delete_review_by_user_id(db=db, user_id=int(user_id))

    return {
        'message': "success delete",
        'status_code': 200,
        'data': f"user_id: {user.id}, user_name: {user.name}, user_email:{user.email} deleted!"
    }


# --- REVIEW --- #
async def delete_review(review_id: int,
                        reason: str = "Нарушение правил сообщества",
                        admin: User = Depends(get_current_admin_user),
                        db: AsyncSession = Depends(get_db)):
    try:
        review = await ReviewDAO.load_review_with_relations(db, review_id)
        CheckHTTP404NotFound(review, "Обзор не найден")

        if await ReviewDAO.is_review_deleted(db, review.id):
            raise HTTPException(status_code=400, detail="Этот обзор уже был удалён ранее.")

        old_review_user_email = review.user.email
        old_review_user_name = review.user.name
        old_review_book_name = review.book.book_name
        old_review_author_name = review.author.name
        old_review_review_title = review.review_title
        old_review_review_body = review.review_body
        old_review_created_date = review.created

        # 1. Создаём запись в deleted_reviews
        deleted_review = await ReviewDAO.create_deleted_review_record(
            db, review, admin, reason
        )

        # 2. Удаляем обзор из reviews
        await db.delete(review)
        await db.commit()

        # 3. Отправляем письмо (через Celery, без await)
        ReviewDAO.notify_user_about_deletion(
            user_name=old_review_user_name,
            user_email=old_review_user_email,
            review_title=old_review_review_title,
            review_body=old_review_review_body,
            created_date=old_review_created_date,
            book_name=old_review_book_name,
            author_name=old_review_author_name,
            reason=reason
        )

        return {
            'message': 'Обзор удален успешно, письмо отправлено',
            'status_code': 200,
            'data': DeletedReviewSchema.from_orm(deleted_review)
        }

    except Exception as e:
        await db.rollback()
        print(f"Ошибка при удалении отзыва: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


# --- AUTHORS --- #
async def add_author(response: Response,
                     request: shema.AuthorCreate,
                     admin: User = Depends(get_current_admin_user),
                     db: AsyncSession = Depends(get_db)):
    author_already_in_db = await AuthorDAO.author_by_name(db=db, author_name=str(request.name.title()))
    if author_already_in_db:
        return {'message': "Автор уже есть в БД!",
                'status_code': 409
                }

    new_author = await AuthorDAO.add_author(request=request, db=db)
    await db.refresh(new_author)

    return {
        'message': "Автор добавлен успешно",
        'status_code': 200,
        'data': {
            'id': new_author.id,
            'author_name': new_author.name
        }
    }


async def change_author(response: Response,
                        author_id: int,
                        request: shema.Author,
                        admin: User = Depends(get_current_admin_user),
                        db: AsyncSession = Depends(get_db)):
    author = await GeneralDAO.get_item_by_id(db=db, item=models.Author, item_id=int(author_id))
    print(author.name)
    CheckHTTP404NotFound(founding_item=author, text="Автор не найден")

    old_author_name = author.name

    print("Author name: ", author.name)
    reviews = await ReviewDAO.get_reviews_by_book_author_id(db=db, review_book_author_id=author.id)
    CheckHTTP404NotFound(founding_item=author, text="Обзоры не найдены")

    author_data, review_data = check_data_for_change_author(request=request, author=old_author_name, reviews=reviews)
    await AuthorDAO.change_author(db=db, author_id=author_id, data=author_data)
    await ReviewDAO.change_reviewed_book_author_name(db=db, old_author_name=old_author_name, r_data=review_data)

    await db.refresh(author)
    for review in reviews:
        await db.refresh(review)

    return {
        'message': "Автор обновлен успешно",
        'status_code': 200,
        'data': {
            'id': author.id,
            'author_name': author.name
        }
    }


async def delete_author(author_id: int,
                        admin: User = Depends(get_current_admin_user),
                        db: AsyncSession = Depends(get_db)):
    author = await GeneralDAO.get_item_by_id(db=db, item=models.Author, item_id=int(author_id))
    CheckHTTP404NotFound(founding_item=author, text="Автор не найден")

    await GeneralDAO.delete_item(db=db, item=models.Author, item_id=int(author_id))

    return {
        'message': "success delete",
        'status_code': 200,
        'data': f"author_id: {author.id},"
                f" author_name: {author.name} deleted!"
    }


# --- REVIEWS --- #
async def change_review(review_id: int,
                        request: shema.ChangeReview,
                        admin: User = Depends(get_current_admin_user),
                        db: AsyncSession = Depends(get_db)):
    review = await GeneralDAO.get_item_by_id(db=db, item=models.Review, item_id=int(review_id))
    CheckHTTP404NotFound(founding_item=review, text="Обзор не найден")

    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(review.created_by))
    CheckHTTP404NotFound(founding_item=user, text="Пользователь не найден")

    new_data = check_data_for_change_review(request=request, review=review)

    await ReviewDAO.change_review(db=db,
                                  review_id=review.id,
                                  data=new_data)

    await db.refresh(review)
    await db.refresh(user)

    return {
        'message': "Обзор обновлен успешно",
        'status_code': 200,
        'data': {
            'id': user.id,
            'author_name': review.reviewed_book_author_name,
            'book_name': review.reviewed_book_name,
            'review_title': new_data.get("review_title"),
            'review_body': new_data.get("review_body")
        }
    }


# --- BOOKS --- #
async def add_book(response: Response,
                   request: shema.BookCreate,
                   admin: User = Depends(get_current_admin_user),
                   db: AsyncSession = Depends(get_db)):
    author = await AuthorDAO.get_author_by_name(db=db, author_name=str(request.book_author_name.title()))
    print(f"Author in back: {author}")
    if not author:
        return {
            'message': "Такой автор не найден",
            'status_code': 404
        }

    if await BookDAO.get_book_by_book_name(book_name=str(request.book_name.capitalize()),
                                           author_id=int(author.id), db=db):
        return {
            'message': "Такая книга уже добавлена",
            'status_code': 404
        }

    book_cover, book_desc = await get_book_info(book_name=request.book_name.capitalize(),
                                                author_name=author.name.title())
    print(f"Обложка: {book_cover}")
    print(f"Описание: {book_desc}")

    if book_cover is None:
        return {
            'message': "Обложка для книги не найдена,"
                       "попробуйте изменить написание названия книги",
            'status_code': 404
        }

    if book_desc is None:
        book_desc = "Описание не добавлено"

    new_book = await BookDAO.add_book(request=request,
                                      book_cover=book_cover,
                                      book_desc=book_desc,
                                      author=author,
                                      db=db)

    await db.refresh(new_book)
    await db.refresh(author)

    return {
        'message': "Книга добавлена успешно",
        'status_code': 200,
        'data': {
            'id': new_book.id,
            'book_cover': new_book.book_cover,
            'book_name': new_book.book_name,
            'book_author_id': new_book.author_id,
            'author_name': author.name,
            'book_description': book_desc
        }
    }


async def delete_book(book_id: int,
                      admin: User = Depends(get_current_admin_user),
                      db: AsyncSession = Depends(get_db)):
    book = await BookDAO.get_book_by_id(db=db, book_id=int(book_id))
    CheckHTTP404NotFound(founding_item=book, text="Книга не найдена")

    await GeneralDAO.delete_item(db=db, item=models.Book, item_id=int(book_id))

    return {
        'message': "success delete",
        'status_code': 200,
        'data': f"book_id: {book.id},"
                f" book_name: {book.book_name} deleted!"
    }


async def change_book(book_id: int,
                      request: shema.Book,
                      admin: User = Depends(get_current_admin_user),
                      db: AsyncSession = Depends(get_db)):
    book = await BookDAO.get_book_by_id(db=db, book_id=int(book_id))
    CheckHTTP404NotFound(founding_item=book, text="Книга не найдена")

    old_book_name = book.book_name

    author = await GeneralDAO.get_item_by_id(db=db, item=models.Author, item_id=int(book.author_id))
    CheckHTTP404NotFound(founding_item=author, text="Автор не найден")

    reviews = await ReviewDAO.get_review_by_book_id(db=db, book_id=int(book.id))

    book_data, review_data = check_data_for_change_book(request=request, book=book, reviews=reviews)

    await BookDAO.change_book(db=db, book_id=int(book.id),
                              new_data=book_data)
    await ReviewDAO.change_reviewed_book_name(db=db,
                                              old_book_name=old_book_name,
                                              r_data=review_data)

    await db.refresh(book)
    for review in reviews:
        await db.refresh(review)

    return {
        'message': "Книга обновлена успешно",
        'status_code': 200,
        'data': {
            'id': book.id,
            'author_name': author.name,
            'book_name': book.book_name,
            'description': book.book_description,
        }
    }


# --- SENDING MAIL --- #
async def send_email_func(request: shema.NewsLetterForUser,
                          db: AsyncSession = Depends(get_db)):
    try:
        await send_email(mail_body=request.mail_body,
                         mail_theme=request.mail_theme,
                         receiver_email=request.receiver_email)
        return {
            'message': 'Письмо отправлено!',
            'status_code': 200,
            'data': {
                'mail_theme': request.mail_theme,
                'mail_body': request.mail_body,
                'mail_receiver': request.receiver_email
            }
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'message': 'Произошла ошибка при отправлении письма!',
            'status_code': 500,
            'data': {
                'mail_theme': request.mail_theme,
                'mail_body': request.mail_body,
                'mail_receiver': request.receiver_email
            }
        }


async def send_newsletter_to_all_users(request: shema.NewsletterForAllUsers,
                                       db: AsyncSession = Depends(get_db)):
    users = await GeneralDAO.get_all_items(db=db, item=models.User)
    errors = []

    for user in users:
        try:
            print(f'Getting user: {user.email}')
            await send_email(mail_theme=request.mail_theme, mail_body=request.mail_body, receiver_email=user.email)
        except Exception as e:
            print(f"Error sending email to {user.email}: {e}")
            errors.append(user.email)

    if errors:
        return {
            'message': f'Рассылка завершена с ошибками для: {", ".join(errors)}',
            'status_code': 100
        }

    return {
        'message': 'Рассылка отправлена всем пользователям',
        'status_code': 200
    }
