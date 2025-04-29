from fastapi import Depends, HTTPException
from sqlalchemy import func

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from backend.src.DAO.general_dao import GeneralDAO
from backend.src.DAO.reviews_dao import ReviewDAO

from backend.src.database.database import get_db
from backend.src.database import models, shema
from backend.src.helpers.general_helper import CheckHTTP404NotFound

from backend.src.helpers.reviews_helper import check_data_for_add_review, check_data_for_change_review

from backend.parsing.get_data import get_book_info


async def create_review(request: shema.Review,
                        response: Response,
                        user: shema.User,
                        db: AsyncSession = Depends(get_db)):

    book, author = await check_data_for_add_review(request=request, db=db)
    new_review = await ReviewDAO.create_review(request=request,
                                               user=user,
                                               book=book,
                                               author=author,
                                               db=db)

    await db.refresh(new_review)
    await db.refresh(user)
    await db.refresh(author)
    await db.refresh(book)
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
                        user: shema.User,
                        db: AsyncSession = Depends(get_db)):
    review = await GeneralDAO.get_item_by_id(db=db, item=models.Review, item_id=review_id)
    CheckHTTP404NotFound(founding_item=review, text="Обзор не найден")

    if not user.is_admin:
        if review.created_by != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет прав для удаления этого обзора")

    await GeneralDAO.delete_item(db=db, item=models.Review, item_id=int(review_id))

    return {
        'message': "success",
        'status_code': 200,
        'status': 'Success',
        'data': {f"Review id:{review.id}",
                 f" title:{review.review_title}",
                 f" book_name:{review.reviewed_book_name} deleted!"
        }
    }


async def get_all_reviews(db: AsyncSession = Depends(get_db)):
    reviews = await GeneralDAO.get_all_items(db=db, item=models.Review)
    CheckHTTP404NotFound(founding_item=reviews, text="Обзоры не найдены")

    reviews_list = []
    for review in reviews:
        book = review.book
        author = review.author

        reviews_list.append({
            'created_by': review.created_by,
            'user': review.user,
            'reviewed_book_id': review.reviewed_book_id,
            'reviewed_book_name': book.book_name,
            'reviewed_book_author_id': review.reviewed_book_author_id,
            'reviewed_book_author_name': author.name,
            'reviewed_book_cover': review.reviewed_book_cover,
            'review_title': review.review_title,
            'review_body': review.review_body,
            'created': review.created,
            'updated': review.updated,
        })

    return reviews_list


async def fetch_review(review_id: int, response: Response, db: AsyncSession = Depends(get_db)):
    review = await GeneralDAO.get_item_by_id(db=db, item=models.Review, item_id=int(review_id))

    CheckHTTP404NotFound(founding_item=review, text="Обзор не найден")

    return review


async def fetch_filtered_review(request: shema.FilteredReview,
                                response: Response,
                                db: AsyncSession = Depends(get_db)):
    reviews = await ReviewDAO.get_filtered_reviews(db=db,
                                                   book_name=request.reviewed_book_name,
                                                   author_name=request.reviewed_author_name)

    CheckHTTP404NotFound(founding_item=reviews, text="Обзоры не найден")

    return reviews
