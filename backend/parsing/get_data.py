from backend.parsing.main_pars import GetBookInfo


async def get_book_info(book_name: str, author_name: str):
    book_cover = GetBookInfo()
    data = await book_cover.get_book_cover_and_description(b_name=book_name, a_name=author_name)

    book_cover_href = data["book_cover_href"]
    book_desc = data["book_description"]

    return book_cover_href, book_desc
