from __future__ import annotations
import re
from typing import List
from selectolax.parser import HTMLParser as SelectoLax

from utilits import get_url


class AsyncHtmlParser:
    """
       Класс для объектов, которые получают html и производят над ним операции: находят бренды, категории, товары и
       считают количество страниц
    """
    categories: list[str]
    products: list[dict]
    brands: list[dict]
    __html: SelectoLax | SelectoLax

    def __init__(self, html: str) -> None:
        """
         Инициализация  объекта AsyncHtmlParser
        """
        self.__html: SelectoLax = SelectoLax(html)
        self.brands: List[dict] = []
        self.products: List[dict] = []
        self.categories: List[str] = []

    async def get_count_pages(self) -> int:
        """
        Метод для получения количества страниц
        """
        pages = self.__html.css_first('.catalog-paginate')
        if pages:
            last_page = int(pages.css('li')[-2].text())
            return last_page
        else:
            return 1

    async def get_current_brand(self) -> str:
        """
        Метод для получения текущего бренда
        """
        brand = self.__html.css_first(
            '.catalog-filters-manufacturer .catalog-checkbox__input[value="true"] + span + span')
        return re.sub('\\s+', ' ', brand.text()).strip()

    async def find_and_set_brands(self) -> None:
        """
        Метод для получения названий и ссылок брендов
        """
        brands = self.__html.css_first('.catalog-filters-manufacturer')
        if brands:
            brands = brands.css('.catalog-checkbox-group__item:not(.is-disabled) .catalog-checkbox__text a')
            for brand in brands:
                brand_name = re.sub('\\s+', ' ', brand.text()).strip()
                brand_url = brand.attributes['href']
                self.brands.append({"name": brand_name, 'url': brand_url})

    async def find_and_set_products(self, brand: dict) -> None:
        """
        Метод для получения товаров по страницам
        """
        products = self.__html.css('#products-wrapper .product-card')
        for product in products:
            product_id = product.attributes['id']
            url = product.css_first('a').attributes['href']
            name = re.sub('\\s+', ' ', product.css_first(
                '.product-card-name__text').text()).strip()
            old_price = product.css_first('.product-unit-prices__old-wrapper .product-price__sum-rubles')
            actual_price = re.findall(r'-[0-9.,]+|[0-9.,]+', product.css_first(
                '.product-unit-prices__actual-wrapper .product-price__sum-rubles').text())
            if not old_price:
                old_price = actual_price
            else:
                old_price = re.findall(r'-[0-9.,]+|[0-9.,]+', old_price.text())
            self.products.append({'brand': brand['name'], 'id': product_id, 'name': name, 'url': url,
                                  'actual_price': "".join(actual_price), 'old_price': "".join(old_price)})

    async def find_and_set_categories(self) -> None:
        """
        Метод для получения списка ссылок на вложенные категории на 1 уровень вглубь. Если получать все ссылки - будет
        слишком много лишних запросов.
        """
        categories = self.__html.css('.catalog-filters-categories > a:not(.is_back)')
        self.categories = [get_url(url.attributes['href']) for url in categories]
