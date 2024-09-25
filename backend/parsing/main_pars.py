import asyncio
import logging
import aiohttp

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# TODO: Create exceptions for returned data, like if parser doesn't find any data - return response about it

class ParsSettings:
    def __init__(self):

        self.base_url = "https://www.bookvoed.ru"
        self.book_name = ""
        self.author_name = ""

        self.search_query = ""
        self.search_url = ""

        self.book_cover = None
        self.book_cover_href = None

        self.response = None
        self.html = None
        self.soup = None
        self.data = {}


class GetData(ParsSettings):
    async def get_data(self, book_name: str, author_name: str):
        if book_name and author_name:
            self.book_name = str(book_name)
            self.author_name = str(author_name)
            self.search_query = f"{self.book_name} {self.author_name}"
            self.search_url = f"{self.base_url}/search?q={self.search_query}"

        else:
            return "No book name and no author name"


class Parser(GetData, ParsSettings):
    async def get_html_page_with_book_cover(self, book_name: str, author_name: str):
        async with aiohttp.ClientSession() as session:
            await self.get_data(book_name=book_name, author_name=author_name)
            print("SEARCH QUERY:", self.search_query)
            print("SEARCH URL:", self.search_url)

            async with session.get(self.search_url) as response:
                self.response = response
                self.html = await response.text()
                print("HTML PRINT: \n", self.html)
                self.soup = BeautifulSoup(self.html, "lxml")

                return self.soup


class GetBookCover(Parser, ParsSettings):
    def __init__(self):
        super().__init__()
        self.images_list = []
        self.images = None
        self.alts = None
        self.book_cover_alt = None

    async def get_book_cover(self):

        self.images = self.soup.find_all('img', attrs={'alt': self.book_name})

        if self.images:
            self.images_list = list(self.images)  # Create a list from the images
            print(self.images_list, sep="\n")
            result_image = self.images_list[0]

            print(result_image['src'])
            self.book_cover_href = result_image['src']

        print(self.book_cover_href)

    async def get_book_cover_href(self, b_name: str, a_name: str):
        try:
            self.soup = await self.get_html_page_with_book_cover(book_name=str(b_name), author_name=str(a_name))
            if self.soup:
                await self.get_book_cover()
                print("Soup True")
                self.data = {
                    'book_cover_href': self.book_cover_href
                }
                print(self.data)
                return self.data
            else:
                print("SOmethig with soup")

        except Exception as e:
            logger.error(f"Error response data: {e}")


# async def main():
#     book_name = "Превращение"
#     author_name = "Франц Кафка"
#     book_cover = GetBookCover()
#     data = await book_cover.get_book_cover_href(b_name=str(book_name), a_name=str(author_name))
#
#     print("Book cover href: ", data["book_cover_href"])
#
#
# if __name__ == '__main__':
#     import asyncio
#
#     asyncio.run(main())
