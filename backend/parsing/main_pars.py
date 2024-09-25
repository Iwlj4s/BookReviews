import asyncio
import logging
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParsSettings:
    def __init__(self):
        self.base_url = "https://www.bookvoed.ru"

        self.book_name = ""
        self.author_name = ""

        self.book_cover = None
        self.book_cover_href = None

        self.data = {}


class GetData(ParsSettings):
    async def get_data(self, book_name: str, author_name: str):
        if book_name and author_name:
            self.book_name = str(book_name),
            self.author_name = str(author_name)

        else:
            return "No book name and no author name"


class Driver(GetData, ParsSettings):
    def __init__(self):
        super().__init__()
        # self.chrome_options = Options()
        # self.chrome_options.add_argument('--ignore-certificate-errors')
        # self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # self.chrome_options.add_argument("--allow-running-insecure-content")
        # self.chrome_options.add_argument("--allow-insecure-localhost")
        # self.chrome_options.add_argument("--disable-web-security")
        # self.chrome_options.add_argument("--incognito")

        # self.chrome_options.add_argument("--headless")  # background start

        self.input = None
        self.search_button = None

        self.driver = None
        self.response = None
        self.html = None
        self.soup = None

    async def initialize_driver(self):
        try:
            self.driver = webdriver.Firefox()
            self.driver.set_page_load_timeout(40)
            logger.info("WebDriver successfully init")
        except Exception as e:
            logger.error(f"Init Error WebDriver: {e}")
            raise

    async def quit_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.warning(f"Close Driver Error: {e}")
            finally:
                self.driver = None

    # Load components func
    async def load_components(self):
        self.input = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-form__input"))
        )
        logger.info("Successfully find input")

        self.search_button = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-form__button-search"))
        )
        logger.info("Successfully find button")

    async def open_url(self):
        try:
            logger.info(f"Try to open URL: {self.base_url}")
            self.driver.get(self.base_url)

        except Exception as e:
            logger.error(f"Page load Error: {e}")
            self.driver.quit()

    async def enter_data(self, book_name: str, author_name: str):
        try:
            self.input.send_keys(book_name + " " + author_name)
            await asyncio.sleep(1)

            self.search_button.click()
            logger.info("Button clicked!")
            await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Data input error: {e}")

    async def get_html_page_with_book_cover(self, book_name: str, author_name: str):
        await self.get_data(book_name=str(book_name), author_name=str(author_name))
        await self.initialize_driver()

        await self.open_url()
        await asyncio.sleep(1)

        await self.load_components()
        await asyncio.sleep(1)

        await self.enter_data(book_name=str(book_name), author_name=str(author_name))
        await asyncio.sleep(1)

        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, "lxml")

        await self.quit_driver()
        self.driver = None

        return self.soup


class GetBookCover(Driver, ParsSettings):
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
        finally:
            await self.quit_driver()


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
