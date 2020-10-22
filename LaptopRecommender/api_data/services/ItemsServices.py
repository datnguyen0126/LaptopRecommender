from api_data.models import Laptop, LaptopId
from api_data.utils import *
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
        item_ids = LaptopId.objects.all()[1:10]
        for item_id in item_ids:
            data = cls.get_product(item_id.id)
            Laptop.objects.create(**data)


