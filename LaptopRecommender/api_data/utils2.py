from bs4 import BeautifulSoup
import re


def has_cpu(text):
    for i in specs_dictionaries.get('cpu'):
        if i in text.lower():
            return True
    return False


def has_ram(text):
    for i in specs_dictionaries.get('ram'):
        if i in text.lower():
            return True
    return False


def has_screen(text):
    for i in specs_dictionaries.get('display'):
        if i in text.lower():
            return True
    return False


def has_disk(text):
    for i in specs_dictionaries.get('disk'):
        if i in text.lower():
            return True
    return False


def has_vga(text):
    for i in specs_dictionaries.get('vga'):
        if i in text.lower():
            return True
    return False


def has_dimension(text):
    for i in specs_dictionaries.get('dimension'):
        if i in text.lower():
            return True
    return False


def has_battery(text):
    for i in specs_dictionaries.get('battery'):
        if i in text.lower():
            return True
    return False


def has_weight(text):
    for i in specs_dictionaries.get('weight'):
        if i in text.lower():
            return True
    return False


specs_dictionaries = {
    'cpu': ['cpu', 'bộ vi xử lý', 'chip', 'bộ vxl'],
    'ram': ['ddr3', 'ddr4', 'ram'],
    'disk': ['ssd', 'hdd'],
    'display': ['13.3', 'inch', '14\'\'', '15.6', 'fhd', 'display'],
    'vga': ["chipset đồ họa", "card đồ họa", "đồ họa", "vga", "Card đồ hoạ", "gpu", "card màn hình"],
    'dimension': [],
    'weight': ['kg'],
    'battery': ['pin']
}

def clean_data(item):
    result = {
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
    description = item.description
    end = description.find('<span')
    temp_description = description[0:end:1]
    #print(temp_description)import re

    texts = re.split('<br />|\n',temp_description)
    for text in texts:
        text = text.strip()
        if not result['cpu'] and has_cpu(text):
            result['cpu'] = text
        if not result['ram'] and has_ram(text):
            result['ram'] = text
        if not result['disk'] and has_disk(text):
            result['disk'] = text
        if not result['vga'] and has_vga(text):
            result['vga'] = text
        if not result['battery'] and has_battery(text):
            result['battery'] = text
        if has_screen(text):
            if not result["display"]:
                result["display"] = text
            if not result["screen_size"]:
                if '15.' in text.lower():
                    result["screen_size"] = 15.6
                    continue
                elif '13.' in text.lower():
                    print(text)
                    result["screen_size"] = 13.3
                    continue
                elif '14.' in text.lower() or '14' in text.lower() or '14\'\'' in text.lower():
                    result["screen_size"] = 14
                    continue
                elif '17.' in text.lower():
                    result["screen_size"] = 17.3
                    continue
        # if (text1.startswith(f[4])):
        #     pass
        # i = text1.index(f[4])
        # str1 = text1.split(':')[1]
        # result['display'] = str1.split(',')[1]
        # result['screen_size'] = str1.split(',')[0]
        # if not item.battery and (text1.startswith(f[5])):
        #     i = text1.index(f[5])
        #     result["battery"] = text1[i:]
    #print(result)

    soup = BeautifulSoup(text, "lxml")
    #print(soup.prettify())
    #s = soup.find_all("span", id=lambda value: value and value.startswith("input_line_"))
    s = soup.findAll('span', {"class": ""})
    #print(soup.find_all("div", id=lambda value: value and value.startswith("input_line_")))
    # for s1 in s:
    #     if(s1.get('data-mention')):
    #         s3 = str(s1.get('data-mention'))
    #         if(f[6] in str(s1.get('data-mention'))):
    #             i = s3.index(f[6])
    #             i1 = s3.index('kg')
    #             result["weight"] = s3[i + 12:i1 + 2]
    #             result["dimension"] = s1.get('data-mention')
    return result
