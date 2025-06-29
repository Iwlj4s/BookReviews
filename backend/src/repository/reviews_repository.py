from fastapi import Depends, HTTPException
from sqlalchemy import func

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from src.DAO.general_dao import GeneralDAO
from src.DAO.reviews_dao import ReviewDAO

from src.database.database import get_db
from src.database import models, shema
from src.database.shema import User
from src.helpers.general_helper import CheckHTTP404NotFound

from src.helpers.reviews_helper import check_data_for_add_review, check_data_for_change_review

from parsing.get_data import get_book_info
from src.repository.admin_repository import get_current_admin_user


# TODO: Fix displaying book's rating in books/book/{book_id}
# TODO: Do adding deleting review in DB DeletedReview


async def create_review(request: shema.ReviewCreate,
                        response: Response,
                        user: shema.User,
                        db: AsyncSession = Depends(get_db)):
    if request.rating and (request.rating < 1 or request.rating > 5):
        raise HTTPException(
            status_code=400,
            detail="Рейтинг должен быть от 1 до 5"
        )

    book, author = await check_data_for_add_review(request=request, db=db)
    new_review = await ReviewDAO.create_review(request=request,
                                               user=user,
                                               book=book,
                                               author=author,
                                               db=db)

    # Refresh all related objects
    await db.refresh(new_review)
    await db.refresh(user)
    await db.refresh(author)
    await db.refresh(book)

    # Ensure we have the latest data
    book = await db.get(models.Book, book.id)
    author = await db.get(models.Author, author.id)

    return {
        'message': "Обзор добавлен успешно",
        'status_code': 200,
        'data': {
            'review_id': new_review.id,
            'Created by': user.id,
            'book_cover': new_review.reviewed_book_cover,
            'book_name': book.book_name,
            'book_id': new_review.reviewed_book_id,
            'book_description': book.book_description,
            'rating': new_review.rating,
            'book_average_rating': book.book_average_rating,
            'author_name': author.name,
            'author_id': new_review.reviewed_book_author_id,
            'review_title': new_review.review_title,
            'review_body': new_review.review_body,
            'created': new_review.created,
        }
    }


async def change_review(review_id: int,
                        request: shema.ChangeReview,
                        user: shema.User,
                        db: AsyncSession = Depends(get_db)):

    review = await GeneralDAO.get_item_by_id(db=db, item=models.Review, item_id=int(review_id))
    CheckHTTP404NotFound(founding_item=review, text="Обзор не найден")

    print("Review created by: ", review.created_by)
    print("User_id: ", user.id)

    if (not user.is_admin) and (review.created_by != user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="У Вас нет прав для изменения этого обзора")

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
            'review_title': new_data.get("review_title"),
            'review_body': new_data.get("review_body"),
            'updated': str(review.updated)
        }
    }


async def delete_review(review_id: int,
                        reason: str = "Нарушение правил сообщества",
                        admin: User = Depends(get_current_admin_user),
                        db: AsyncSession = Depends(get_db)):
    """
    :param review_id: deleting review's id
    :param reason: deleting reason
    :param admin: is user admin
    :param db: database
    :return: deleted review + message successfully sent email

    Loading deleting review
    Saving needed data before deleting review
    Creating deleted review in table deleted_review
    Delete review from reviews table
    Send notify user about deleted review
    """
    try:
        review = await ReviewDAO.load_review_with_relations(db, review_id)
        CheckHTTP404NotFound(review, "Обзор не найден")

        review_id = review.id
        user_email = review.user.email
        user_name = review.user.name
        book_name = review.book.book_name
        author_name = review.author.name
        review_title = review.review_title
        review_body = review.review_body
        created_date = review.created

        deleted_review = await ReviewDAO.create_deleted_review_record(
            db, review, admin, reason
        )

        print("Обзор удален")

        ReviewDAO.notify_user_about_deletion(user_name=user_name,
                                                   user_email=user_email,
                                                   review_title=review_title,
                                                   review_body=review_body,
                                                   created_date=created_date,
                                                   book_name=book_name,
                                                   author_name=author_name,
                                                   reason=reason)
        return {
            'message': 'Обзор удален успешно, письмо отправлено',
            'status_code': 200,
            'data': deleted_review
        }

    except Exception as e:
        await db.rollback()
        print(f"Ошибка при удалении отзыва: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


async def get_all_reviews(db: AsyncSession = Depends(get_db)):
    reviews = await ReviewDAO.get_reviews_desc(db=db)
    CheckHTTP404NotFound(founding_item=reviews, text="Обзоры не найдены")

    reviews_list = []
    from backend.src.routes.users_router import review_to_out
    for review in reviews:
        reviews_list.append(await review_to_out(review))

    return reviews_list


async def fetch_review(review_id: int, response: Response, db: AsyncSession = Depends(get_db)):
    review = await GeneralDAO.get_item_by_id(db=db, item=models.Review, item_id=int(review_id))

    CheckHTTP404NotFound(founding_item=review, text="Обзор не найден")

    from backend.src.routes.users_router import review_to_out
    return await review_to_out(review)


async def fetch_filtered_review(request: shema.FilteredReview,
                                response: Response,
                                db: AsyncSession = Depends(get_db)):
    reviews = await ReviewDAO.get_filtered_reviews(db=db,
                                                   book_name=request.reviewed_book_name,
                                                   author_name=request.reviewed_author_name)

    CheckHTTP404NotFound(founding_item=reviews, text="Обзоры не найден")

    from backend.src.routes.users_router import review_to_out
    reviews_list = [await review_to_out(r) for r in reviews]
    return reviews_list
