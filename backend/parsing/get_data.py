from backend.parsing.main_pars import GetBookCover


async def get_book_cover(book_name: str, author_name: str):
    book_cover = GetBookCover()
    data = await book_cover.get_book_cover_href(b_name=book_name, a_name=author_name)

    book_cover_href = data["book_cover_href"]
    print("Book cover href from get data file: ", book_cover_href)

    return book_cover_href
