from bs4 import BeautifulSoup
from django.db import IntegrityError

from api_data.utils import *
from api_data.models import LaptopId
import requests, json

LAPTOP_URL = "https://tiki.vn/laptop/c8095?src=c.8095.hamburger_menu_fly_out_banner&page={page}"
product_url = "https://tiki.vn/api/v2/products/{}"


class ListDataServices:

    @classmethod
    def get_product_id(cls):
        product_list = []
        i = 1
        while True:
            print("Crawl page: ", i)
            source = requests.get(LAPTOP_URL.format(page=i), headers=FAKE_HEADER).text
            parser = BeautifulSoup(source, 'lxml')

            product_ids_list = parser.findAll(class_="product-item")

            if len(product_ids_list) == 0:
                break

            for product in product_ids_list:
                product_list.append(product.get("data-id"))
                try:
                    LaptopId.objects.create(id=product.get("data-id"), link=product.contents[1].get('href'))
                except IntegrityError:
                    continue

            i += 1

        return product_list, i

    @classmethod
    def start_get_list(cls):
        cls.get_product_id()

    @classmethod
    def get_thumnails(cls):
        laptop_ids = LaptopId.objects.all()
        for laptop in laptop_ids:
            source = requests.get(product_url.format(laptop.id), headers=FAKE_HEADER).text
            data = json.loads(source)
            laptop.thumbnails = data.get('thumbnail_url')
            laptop.save()

