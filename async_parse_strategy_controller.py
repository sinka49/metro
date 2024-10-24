import asyncio
from typing import List
import aiohttp
from tqdm import tqdm

from async_csv_writer import AsyncCsvWriter
from async_html_parser import AsyncHtmlParser
from constants import CATEGORY, HEADERS
from utilits import get_url


class AsyncParseStrategyController:
    """
    Класс для объекта стратегии парсинга
    """
    csv_writer: AsyncCsvWriter
    category: str
    count_products: int

    def __init__(self) -> None:
        self.count_products: int = 0
        self.category: str = CATEGORY
        self.csv_writer: AsyncCsvWriter = AsyncCsvWriter()

    # Метод для получения хтмл по ссылке
    @staticmethod
    async def get_html_docs(urls: List[str]) -> list[str]:
        """
        Метод для получения html страниц по ссылкам
        """
        async with aiohttp.ClientSession(trust_env=True) as session:
            tasks = []
            for url in urls:
                tasks.append(asyncio.create_task(session.get(url, headers=HEADERS)))
            responses = await asyncio.gather(*tasks)
            return [await r.text(encoding='UTF-8') for r in responses]

    async def start_parsing(self) -> None:
        """
        Метод для описания стратегии начала парсинга.
        Так как категория может быть общей и не содержать фильтра по брендам, собираем список категорий,
        которые теоретически могут содержать фильтр бренда. Сейчас все категории второго уровня содержат бренд. Но это
        не точно) Не соответствует принципу ягни, но тут как будто бы лучше перебдеть.
        """
        print(f'\nПроверяем категорию {CATEGORY}.')
        url = get_url(CATEGORY)
        brand_position = url.find('/brend/')
        html_docs = await self.get_html_docs([url])
        parser = AsyncHtmlParser(html_docs[0])
        if brand_position > -1:
            brand = {'name': await parser.get_current_brand(), 'url': CATEGORY}
            print(f'Данная категория - бренд {brand["name"]}')
            await parser.find_and_set_products(brand)
            self.count_products += len(parser.products)
            await self.csv_writer.write_to_csv(parser.products)
            count_pages = await parser.get_count_pages()
            if count_pages > 1:
                await self.__parse_brands_by_pages(count_pages, brand)
        else:
            await parser.find_and_set_brands()
            brands = parser.brands
            if len(brands):
                print(f'Данная категория содержит фильтр по брендам.')
                await self.__parse_category_by_brands(brands, True)
            else:
                await parser.find_and_set_categories()
                print(f'Данная категория содержит вложенные катеогории и не содержит фильтр по брендам.')
                await self.__parse_category_recursive(parser.categories, True)

    async def __parse_category_recursive(self, categories: List[str], pbar: bool = False) -> None:
        """
        Метод для рекурсивного прохода по категориям в поисках бренда
        """

        html_docs = await self.get_html_docs(categories)
        __INFO_CATEGORIES_PBAR = f'Ищу товары по брендам по вложенным {len(html_docs)} категориям'
        html_docs_pbar = tqdm(html_docs, colour='GREEN', desc=__INFO_CATEGORIES_PBAR, ncols=120) if pbar else html_docs
        for index, html in enumerate(html_docs_pbar):
            parser = AsyncHtmlParser(html)
            await parser.find_and_set_brands()
            brands = parser.brands
            if len(brands):
                await self.__parse_category_by_brands(brands)
            else:
                await parser.find_and_set_categories()
                await self.__parse_category_recursive(parser.categories)

    async def __parse_category_by_brands(self, brands: List[dict], pbar: bool = False) -> None:
        """
        Метод для получения товаров по брендам. Собираем ссылки на фильтрацию по брендам (Чтобы не
        ходить по каждому товару в поисках бренда) и по списку брендов получаем товары с первой страницы
        бренда. Запускаем парсинг по страницам бренда.
        """

        page = 1
        urls = [get_url(brand['url'], page) for brand in brands]
        __INFO_BRANDS_PBAR = f'Ищу товары по {len(urls)} брендам в этой категории'
        html_docs = await self.get_html_docs(urls)
        html_docs_pbar = tqdm(html_docs, colour='GREEN', desc=__INFO_BRANDS_PBAR, ncols=120) if pbar else html_docs
        for index, html in enumerate(html_docs_pbar):
            parser = AsyncHtmlParser(html)
            await parser.find_and_set_products(brands[index])
            self.count_products += len(parser.products)
            await self.csv_writer.write_to_csv(parser.products)
            count_pages = await parser.get_count_pages()
            if count_pages > 1:
                await self.__parse_brands_by_pages(count_pages, brands[index])

    # проверяем парсером пагинацию. Если вернет больше 1 - запустится цикл прохождения по страницам
    async def __parse_brands_by_pages(self, count_pages, brand: dict) -> None:
        """
        Метод для получения товаров по страницам пагинации.
        """
        urls = [get_url(brand['url'], p) for p in range(2, count_pages + 1)]
        html_docs = await self.get_html_docs(urls)
        for html in html_docs:
            parser = AsyncHtmlParser(html)
            await parser.find_and_set_products(brand)
            await self.csv_writer.write_to_csv(parser.products)
            self.count_products += len(parser.products)
