from django.db import IntegrityError

from api_data.models import Laptop, LaptopId, LaptopBackup
from api_data.utils import *
from api_data.utils2 import *
import requests, json

API_GET_ITEM = "https://tiki.vn/api/v2/products/{id}"

class DataServices:

    @classmethod
    def get_product(cls, item_id):
        result = {}
        url = API_GET_ITEM.format(id=item_id)
        response = requests.get(url, headers=FAKE_HEADER)
        try:
            if response.status_code == 200:
                data = json.loads(response.text)
                for field in ITEM_FIELDS:
                    if field != ITEM_FIELDS[-1]:
                        result[field] = data.get(field)
                    else:
                        specs_data = data.get(ITEM_FIELDS[-1])
                        if specs_data:
                            specs_data = get_specifications(specs_data)
                            result = { **result, **specs_data }
            return result
        except Exception:
            return

    @classmethod
    def start_get_items(cls):
        item_ids = LaptopId.objects.all()
        for item_id in item_ids:
            data = cls.get_product(item_id.id)
            print('Getting product: ', item_id.id)
            try:
                Laptop.objects.create(**data)
            except IntegrityError:
                continue

    @classmethod
    def backup_data(cls):
        queryset = Laptop.objects.all()
        for item in queryset:
            if not (item.cpu and item.dimension and item.weight and item.ram):
                temp_laptop = LaptopBackup()
                temp_laptop.__dict__ = item.__dict__.copy()
                temp_laptop.save()

    @classmethod
    def clean_data(cls):
        queryset = LaptopBackup.objects.all()
        for item in queryset:
            res = clean_data(item)
            if not item.cpu:
                item.cpu = res.get('cpu')
            if not item.ram:
                item.ram = res.get('ram')
            if not item.vga:
                item.vga = res.get('vga')
            if not item.disk:
                item.disk = res.get('disk')
            if not item.display:
                item.display = res.get('display')
            if not item.screen_size:
                item.screen_size = res.get('screen_size')
            if not item.battery:
                item.battery = res.get('battery')
            item.save()

    @classmethod
    def restore_data(cls):
        items = LaptopBackup.objects.all()
        for item in items:
            temp_laptop = Laptop()
            temp_laptop.__dict__ = item.__dict__.copy()
            temp_laptop.save()

