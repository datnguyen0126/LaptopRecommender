FAKE_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Accept': '*/*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://shopee.vn/',
    'X-Shopee-Language': 'vi',
    'X-Requested-With': 'XMLHttpRequest',
    'X-API-SOURCE': 'pc'
}

ITEM_FIELDS = ["id", "description", "name", "price", "stock", "rating_average", "review_count", "specifications"]

def get_value_of_property(item, property):
    if property == "rating_star":
        return item.get('item_rating').get('rating_star')
    if property == "rating_count":
        scores = []
        for score in item.get('item_rating').get('rating_count'):
            scores.append(score)
        return '-'.join(map(str, scores))
    else:
        return item.get(property)


# only works for tiki
def get_specifications(specs):
    attributes = {
        "Thông tin chung": ["Thương hiệu", "Kích thước", "Trọng lượng"],
        "Bộ xử lý": ["CPU", "Chip set", "Hệ điều hành"],
        "Màn hình": ["Độ phân giải", "Kích thước màn hình", "Loại/ Công nghệ màn hình"],
        "Đồ họa": ["Card đồ họa"],
        "Đĩa cứng": ["Dung lượng ổ cứng", "Loại ổ đĩa"],
        "Bộ nhớ": ["RAM", "Loại RAM", "Bus"],
        "Thông tin pin": ["Loại pin"]
    }
    result = {
        "brand": '',
        "dimension": '',
        "weight": '',
        "cpu": '',
        "display": '',
        "screen_size": '',
        "vga": '',
        "disk": '',
        "ram": '',
        "battery": ''
    }
    result_fields = list(result.keys())
    title = list(attributes.keys())
    for spec in specs:
        if spec.get('name') == title[0]:
            fields = attributes.get(title[0])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[0]] = attr.get('value')
                elif attr.get('name') == fields[1]:
                    result[result_fields[1]] = attr.get('value')
                elif attr.get('name') == fields[2]:
                    result[result_fields[2]] = attr.get('value')

        if spec.get('name') == title[1]:
            fields = attributes.get(title[1])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[3]] = attr.get('value')
                if attr.get('name') == fields[1]:
                    result[result_fields[3]] = result[result_fields[3]] + " " + attr.get('value')

        if spec.get('name') == title[2]:
            fields = attributes.get(title[2])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[4]] = attr.get('value')
                elif attr.get('name') == fields[1]:
                    result[result_fields[5]] = attr.get('value')

        if spec.get('name') == title[3]:
            fields = attributes.get(title[3])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[6]] = attr.get('value')

        if spec.get('name') == title[4]:
            fields = attributes.get(title[4])
            for attr in spec.get('attributes'):
                result[result_fields[7]] = result[result_fields[7]] + "&" + attr.get('value')

        if spec.get('name') == title[5]:
            fields = attributes.get(title[5])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[8]] = attr.get('value')

        if spec.get('name') == title[6]:
            fields = attributes.get(title[6])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[9]] = attr.get('value')

    return result
