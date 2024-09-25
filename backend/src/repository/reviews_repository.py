from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from backend.src.DAO.general_dao import GeneralDAO
from backend.src.DAO.reviews_dao import ReviewDAO

from backend.src.database.database import get_db
from backend.src.database import models, shema
from backend.src.helpers.general_helper import CheckHTTP404NotFound

from backend.src.helpers.reviews_helper import check_data_for_add_review, check_data_for_change_review

from backend.parsing.get_data import get_book_cover


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
    return {
        'message': "Обзор добавлен успешно",
        'status_code': 200,
        'data': {
            'Created by': user.id,
            'Обложка': new_review.reviewed_book_cover,
            'Книга': new_review.reviewed_book_name,
            'id Автора': author.id,
            'Автор': new_review.reviewed_book_author_name,
            'Заголовок': new_review.review_title,
            'Обзор': new_review.review_body
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

    if review.created_by != user.id:
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
            'Автор': review.reviewed_book_author_name,
            'Книга': review.reviewed_book_name,
            'Заголовок': new_data.get("review_title"),
            'Обзор': new_data.get("review_body")
        }
    }


async def delete_review(review_id: int,
                        user: shema.User,
                        db: AsyncSession = Depends(get_db)):
    review = await GeneralDAO.get_item_by_id(db=db, item=models.Review, item_id=review_id)
    CheckHTTP404NotFound(founding_item=review, text="Обзор не найден")

    if review.created_by != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет прав для удаления этого обзора")

    await GeneralDAO.delete_item(db=db, item=models.Review, item_id=int(review_id))

    return {
        'message': "success",
        'status_code': 200,
        'status': 'Success',
        'data': f"Review id:{review.id} title:{review.review_title} book_name:{review.reviewed_book_name} deleted!"
    }


async def get_all_reviews(db: AsyncSession = Depends(get_db)):
    reviews = await GeneralDAO.get_all_items(db=db, item=models.Review)

    CheckHTTP404NotFound(founding_item=reviews, text="Обзоры не найден")

    return reviews


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
