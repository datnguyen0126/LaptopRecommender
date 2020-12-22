import operator
import re
from functools import reduce

from django.db.models import Q

from api.utils import Utils
from api_result.models import ClusteringScores, TrainData


class WeightCluster:
    k = 9

    option = ["Very light", "Medium", "Don't bother"]
    series = {
        'light': ['zenbook', 'macbook', 'gram', 'spectre', 'elitebook', 'xps', 'swift', 'yoga', 'thinkbook', 'slim', 'envy', 'modern'],
        'medium': ['vostro', 'inspiron', 'aspire', 'latitude', 'vivobook', 'thinkpad', 'ideapad', 'pavilion', 'probook']
    }

    @classmethod
    def weight_cluster(cls, laptop_queryset, answer):
        if answer == cls.option[0]: #
            ids = []
            for laptop in laptop_queryset:
                if not laptop.weight:
                    if cls.in_list_keyword(laptop.name, cls.series.get('light')) and laptop.price > 15000000:
                        ids.append(laptop.id)
                        continue
                if cls.extract_size(laptop.screen_size) > 15:
                    if cls.extract_values(laptop.weight)[0] < 1.8:
                        ids.append(laptop.id)
                else:
                    if cls.extract_values(laptop.weight)[0] < 1.4:
                        ids.append(laptop.id)
            return laptop_queryset.filter(id__in=ids)
        if answer == cls.option[1]:
            ids = []
            for laptop in laptop_queryset:
                if not laptop.weight:
                    if cls.in_list_keyword(laptop.name, cls.series.get('medium')):
                        ids.append(laptop.id)
                        continue
                if cls.extract_size(laptop.screen_size) > 15:
                    if cls.extract_values(laptop.weight)[0] < 2.4:
                        ids.append(laptop.id)
                else:
                    if cls.extract_values(laptop.weight)[0] < 2.0:
                        ids.append(laptop.id)
            return laptop_queryset.filter(id__in=ids)
        if answer == cls.option[2]:
            return laptop_queryset

    @classmethod
    def in_list_keyword(cls, text, keywords):
        for key in keywords:
            if key in text:
                return True
        return False

    @classmethod
    def extract_values(cls, text, key='weight'): # cm for dimension and kg for weight
        try:
            text = text.replace(',', '.')
            pattern = '\d*\.?\d+'
            values = re.findall(pattern, text)
            ret = []
            if key == 'dimension':
                for value in values:
                    value = Utils.convert_to_float(value)
                    if 'mm' in text:
                        value = value / 1000
                    ret.append(value)
            if key == 'weight':
                value = Utils.convert_to_float(values[0])
                if value > 50 and 'kg' not in text and 'g' in text:
                    value = value / 1000
                ret.append(value)
            return ret
        except Exception:
            return [0]

    @classmethod
    def extract_size(cls, screen_size):
        try:
            pattern = '\d*[\.|,]?\d+'
            ssize = re.findall(pattern, screen_size)[0]
            return float(ssize)
        except Exception:
            return 0

    @classmethod
    def distance(cls, check_laptop, train_laptop):
        laptop1_dimensions = cls.extract_values(check_laptop.dimension, 'dimension')
        laptop2_dimensions = cls.extract_values(train_laptop.dimension, 'dimension')
        laptop1_weight = cls.extract_values(check_laptop.weight, 'weight')
        laptop2_weight = cls.extract_values(train_laptop.weight, 'weight')
        laptop1_screen_size = cls.get_value(check_laptop.screen_size)
        laptop2_screen_size = cls.get_value(train_laptop.screen_size)

        x1 = laptop1_dimensions[0]
        x2 = laptop2_dimensions[0]
        y1 = laptop1_dimensions[1]
        y2 = laptop2_dimensions[1]
        z1 = laptop1_dimensions[2]
        z2 = laptop2_dimensions[2]
        w1 = laptop1_weight[0]
        w2 = laptop2_weight[0]
        s1 = laptop1_screen_size
        s2 = laptop2_screen_size

        return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2) + (w1 - w2) * (w1 - w2) + (s1 - s2) * (s1 - s2)

    @classmethod
    def check_laptop(cls, purpose, laptop):
        train_data = TrainData.objects.filter(answer_name__icontains=purpose)
        nearest = [None] * cls.k
        for item in train_data:
            if item == laptop:
                return True
            temp = dict(check=item.check, distance=cls.distance(laptop, item))
            if temp['distance'] == -1:
                return True
            for i in range(len(nearest)):
                if nearest[i] is None:
                    break
                else:
                    if nearest[i]['distance'] > temp['distance']:
                        if i != len(nearest) - 1:
                            nearest[i + 1] = nearest[i]
            nearest[i] = temp
        yes = 0
        for i in nearest:
            if i['check']:
                yes = yes + 1
        if yes > cls.k / 2:
            return True
        return False