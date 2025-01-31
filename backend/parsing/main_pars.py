import asyncio
import logging
import aiohttp

from bs4 import BeautifulSoup

import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParsSettings:
    def __init__(self):
        self.base_url = "https://www.bookvoed.ru"
        self.book_name = ""
        self.author_name = ""

        self.search_query = ""
        self.search_url = ""

        self.response = None
        self.html = None
        self.soup = None


class GetData(ParsSettings):
    async def get_data(self, book_name: str, author_name: str):
        if book_name and author_name:
            self.book_name = str(book_name)
            self.author_name = str(author_name)
            self.search_query = f"{self.author_name} {self.book_name}"
            self.search_url = f"{self.base_url}/search?q={self.search_query}"
        else:
            return "No book name and no author name"


class Parser(GetData, ParsSettings):
    async def get_html_page_with_book_cover(self, book_name: str, author_name: str):
        async with aiohttp.ClientSession() as session:
            await self.get_data(book_name=book_name, author_name=author_name)
            async with session.get(self.search_url) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch data: {response.status}")
                    return None
                self.response = response
                self.html = await response.text()
                self.soup = BeautifulSoup(self.html, "lxml")
                return self.soup

    async def get_book_details(self, book_href: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(book_href) as response:
                self.response = response
                self.html = await response.text()
                self.soup = BeautifulSoup(self.html, "lxml")
                return self.soup


class GetBookInfo(Parser, ParsSettings):
    async def get_book_cover_and_description(self, b_name: str, a_name: str):
        self.soup = await self.get_html_page_with_book_cover(book_name=b_name, author_name=a_name)
        if not self.soup:
            logger.error("Could not retrieve soup object.")
            return None

        book_link = self.soup.find('a', attrs={'href': re.compile(r'/product/')})
        if book_link:
            book_href = f"{self.base_url}{book_link['href']}"
            details_soup = await self.get_book_details(book_href)

            description_tag = details_soup.find('div', class_='product-annotation-full__text')
            if description_tag:
                description = ' '.join([p.get_text(strip=True) for p in description_tag.find_all('p')])
                if not description:
                    description = "Описание отсутствует"
            else:
                description = "Описание отсутствует"

            image_tag = details_soup.find('img', class_='product-preview__big-img')
            image_src = image_tag['src'] if image_tag else None

            return {
                'book_href': book_href,
                'book_description': description,
                'book_cover_href': image_src
            }
        else:
            logger.error("Could not find book link.")


# async def main():
#     book_name = "письма к милене"
#     author_name = "Франц Кафка"
#     book_info = GetBookInfo()
#     data = await book_info.get_book_cover_and_description(b_name=book_name, a_name=author_name)
#
#     if data:
#         print("Book href: ", data['book_href'])
#         print("Description: ", data['book_description'])
#         print("Image source: ", data['book_cover_href'])
#     else:
#         print("Failed to retrieve book information.")
#
#
# if __name__ == '__main__':
#     import asyncio
#
#     asyncio.run(main())
