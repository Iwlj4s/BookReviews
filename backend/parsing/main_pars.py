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

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }

        self.cookies = {
            'sessionid': 'some_random_session_id',
            'csrftoken': 'some_random_csrf_token'
        }


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
        async with aiohttp.ClientSession(headers=self.headers, cookies=self.cookies) as session:
            await self.get_data(book_name=book_name, author_name=author_name)
            logger.info(f"Search URL: {self.search_url}")
            async with session.get(self.search_url) as response:
                self.response = response
                self.html = await response.text()
                self.soup = BeautifulSoup(self.html, "lxml")
                print("HTML IN get_html_page_with_book_cover:\n", self.html)
                return self.soup

    async def get_book_details(self, book_href: str):
        async with aiohttp.ClientSession(headers=self.headers, cookies=self.cookies) as session:
            logger.info(f"Book details URL: {book_href}")
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
        
        product_cards = self.soup.find_all('div', class_='product-card')
        logger.info(f"Found {len(product_cards)} product cards")
        
        if not product_cards:
            logger.error("No product cards found")
            return None
        
        first_product = product_cards[0]

        book_link = first_product.find('a', href=re.compile(r'/product/'))
        logger.info(f"Book link found: {book_link['href'] if book_link else 'None'}")

        if book_link:
            book_href = f"{self.base_url}{book_link['href']}"
            logger.info(f"Book href found: {book_href}")
            
            details_soup = await self.get_book_details(book_href)
            description = "Описание отсутствует"
            description_tag = details_soup.find('div', class_='product-annotation-full__text')
            if description_tag:
                description = description_tag.get_text(separator=' ', strip=True)
                logger.info(f"Description found: {description[:200]}...")

            image_tag = details_soup.find('img', class_='product-preview__big-img')
            image_src = image_tag['src'] if image_tag else None
            logger.info(f"Image src: {image_src}")

            return {
                'book_href': book_href,
                'book_description': description,
                'book_cover_href': image_src
            }
        else:
            logger.error("Could not find book link.")
            return None

# async def main():
#     book_name = "письма к милене"
#     author_name = "Франц Кафка"
#     book_info = GetBookInfo()
#     data = await book_info.get_book_cover_and_description(b_name=book_name, a_name=author_name)

#     if data:
#         print("Book href: ", data['book_href'])
#         print("Description: ", data['book_description'])
#         print("Image source: ", data['book_cover_href'])
#     else:
#         print("Failed to retrieve book information.")

# if __name__ == '__main__':
#     asyncio.run(main())
