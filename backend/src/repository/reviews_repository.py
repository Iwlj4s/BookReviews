from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from backend.src.DAO.reviews_dao import ReviewDAO
from backend.src.DAO.users_dao import UserDAO

from backend.src.database.database import get_db
from backend.src.database import models, shema
from backend.src.helpers.general_helper import CheckHTTP404NotFound, CheckHTTP401Unauthorized

from backend.src.helpers.reviews_helper import check_data_for_add_review
from backend.src.helpers.token_helper import get_token, verify_token


# TODO: Add change review function
async def create_review(request: shema.Review,
                        response: Response,
                        token: str = Depends(get_token),
                        db: AsyncSession = Depends(get_db)):
    user_id = verify_token(token=token)

    user = await UserDAO.get_user_by_id(db=db, user_id=int(user_id))
    await CheckHTTP401Unauthorized(founding_item=user, text="Пользователь не найден")

    book, author = await check_data_for_add_review(request=request, db=db)

    new_review = models.Review(
        created_by=user_id,
        reviewed_book_id=book.id,
        reviewed_book_name=book.book_name,
        reviewed_book_author_name=author.name,
        review_title=request.review_title,
        review_body=request.review_body
    )

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)

    return new_review


async def delete_review(review_id: int,
                        db: AsyncSession = Depends(get_db),
                        token: str = Depends(get_token)):

    user_id = verify_token(token=token)
    user = await UserDAO.get_user_by_id(db=db, user_id=int(user_id))
    user = await CheckHTTP404NotFound(founding_item=user, text="Пользователь не найден")

    review = await ReviewDAO.get_review_by_id(db=db, review_id=review_id)
    review = await CheckHTTP404NotFound(founding_item=review, text="Обзор не найден")

    if review.created_by != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет прав для удаления этого обзора")

    await ReviewDAO.delete_review(db=db, review_id=review_id)

    return {
        'message': "success",
        'status_code': 200,
        'status': 'Success',
        'data': f"Review id:{review.id} title:{review.review_title} book_name:{review.reviewed_book_name} deleted!"
    }


async def get_all_reviews(db: AsyncSession = Depends(get_db)):
    reviews = await ReviewDAO.get_all_reviews(db=db)

    reviews = await CheckHTTP404NotFound(founding_item=reviews, text="Обзоры не найден")

    return reviews


async def fetch_review(review_id: int, response: Response, db: AsyncSession = Depends(get_db)):
    review = await ReviewDAO.get_review_by_id(db=db, review_id=review_id)

    review = await CheckHTTP404NotFound(founding_item=review, text="Обзор не найден")

    return review


async def fetch_filtered_review(request: shema.FilteredReview,
                                response: Response,
                                db: AsyncSession = Depends(get_db)):

    reviews = await ReviewDAO.get_filtered_reviews(db=db,
                                                   book_name=request.reviewed_book_name,
                                                   author_name=request.reviewed_author_name)

    reviews = await CheckHTTP404NotFound(founding_item=reviews, text="Обзоры не найден")

    return reviews
