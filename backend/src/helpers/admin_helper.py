from backend.src.database import shema


def check_data_for_change_author(request: shema.Author, author, reviews):
    author_data = {}
    review_data = {}

    if request.name is None:
        author_data.update({"name": author})
    else:
        author_data.update({"name": request.name})

    for review in reviews:
        review_data.update({
            "reviewed_book_author_name": request.name if request.name else review.reviewed_book_author_name,
        })

    return author_data, review_data


def check_data_for_change_book(request: shema.Book, book, reviews):
    book_data = {}
    review_data = {}

    if request.book_description is None:
        book_data.update({"book_description": book.book_description})
    else:
        book_data.update({"book_description": request.book_description})

    for review in reviews:
        review_data.update({
            "book_name": request.book_name if request.book_name else review.reviewed_book_name,
        })
        book_data.update({
            "book_name": request.book_name if request.book_name else review.reviewed_book_name,
        })

    return book_data, review_data