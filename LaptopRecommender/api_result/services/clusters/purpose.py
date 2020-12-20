import operator
from functools import reduce
from multiprocessing import Value

from django.db.models import Q, F
from django.db.models.functions import Concat

from api_data.models import Laptop
from api.utils import Utils
from api_questions.models import Answers
from api_result.models import ClusteringScores, TrainData
from api_questions.constants import Questions
from api_result.services.ExtractDataService import ExtractDataService


class PurposeCluster:
    k = 5
    options = Questions.QUESTIONS[1]["options"]
    # "Web browsing",
    # "Document",
    # "Watching Movies",
    # "Light Gaming",
    # "Heavy Gaming",
    # "Photo editing (pro)",
    # "Photo editing (basic)",
    # "Video production",
    # "3D design",
    # "Programming"

    @classmethod
    def get_answer_index(cls, purpose_answer):
        ret = {}
        i = 0
        for option in cls.options:
            for purpose in purpose_answer:
                if purpose == option:
                    ret[i] = True
            i += 1
        return ret

    @classmethod
    def cluster_purpose(cls, laptops, purpose_answer, money_answer):
        answers = cls.get_answer_index(purpose_answer)
        print(answers)
        if answers.get(0):
            laptops = cls.get_Web_browsing(laptops, money_answer)
        if answers.get(1):
            laptops = cls.get_Document(laptops, money_answer)
        if answers.get(2):
            laptops = cls.get_Watching_Movies(laptops, money_answer)
        if answers.get(3):
            laptops = cls.get_Light_Gaming(laptops, money_answer)
        if answers.get(4):
            laptops = cls.get_Heavy_Gaming(laptops, money_answer)
        if answers.get(5):
            laptops = cls.get_Photo_editing_pro(laptops, money_answer)
        if answers.get(6):
            laptops = cls.get_Photo_editing_basic(laptops, money_answer)
        if answers.get(7):
            laptops = cls.get_Video_production(laptops, money_answer)
        if answers.get(8):
            laptops = cls.get_3D_design(laptops, money_answer)
        if answers.get(9):
            laptops = cls.get_programming(laptops, money_answer)
        return laptops

    @classmethod
    def get_Web_browsing(cls, laptops_queryset, money_answer):
        return laptops_queryset

    @classmethod
    def get_Document(cls, laptops_queryset, money_answer):
        search_words = ['1TB', '512GB']
        return laptops_queryset.filter(reduce(operator.or_, (Q(disk__icontains=x) for x in search_words)))

    @classmethod
    def get_Watching_Movies(cls, laptops_queryset, money_answer):
        search_words = ['full hd', '1080', '1440', 'fullhd', 'ips']
        laptops_queryset = laptops_queryset.filter(reduce(operator.or_, (Q(display__icontains=x) for x in search_words)))
        large_macbook = ExtractDataService.get_macbook(small=False, price=money_answer)
        return laptops_queryset | large_macbook

    @classmethod
    def get_Light_Gaming(cls, laptops_queryset, money_answer):
        search_vga = ['nvidia', 'amd', 'rtx', 'gtx']
        laptops_queryset = laptops_queryset.filter(reduce(operator.or_, (Q(vga__icontains=x) for x in search_vga)))\
                                                        .exclude(cpu__icontains='ryzen 3', name__icontains='macbook')
        laptops_queryset = ExtractDataService.ram_filter(laptops_queryset, min=7)
        return laptops_queryset

    @classmethod
    def get_Heavy_Gaming(cls, laptops_queryset, money_answer):  # -------------------------------------------------
        answer = Answers.objects.filter(content__icontains='heavy gaming').first()
        laptops_queryset = laptops_queryset.filter(purpose_group__icontains=str(answer.id))

        return laptops_queryset

    @classmethod
    def get_Photo_editing_pro(cls, laptops_queryset, money_answer): # ---------------------------------------------------
        return cls.get_Video_production(laptops_queryset, money_answer)

    @classmethod
    def get_Photo_editing_basic(cls, laptops_queryset, money_answer):
        search_vga = ['nvidia', 'amd', 'rtx', 'gtx']
        laptops_queryset = laptops_queryset.filter(reduce(operator.or_, (Q(vga__icontains=x) for x in search_vga)))\
                                                        .exclude(cpu__icontains='ryzen 3', name__icontains='macbook')
        laptops_queryset = ExtractDataService.ram_filter(laptops_queryset, min=7)
        return laptops_queryset

    @classmethod
    def get_Video_production(cls, laptops_queryset, money_answer):  # ------------------------------------------------------------
        answer = Answers.objects.filter(content__icontains='video production').first()
        laptops_queryset = laptops_queryset.filter(purpose_group__icontains=str(answer.id))

        return laptops_queryset

    @classmethod
    def get_3D_design(cls, laptops_queryset, money_answer):
        search_vga = ['quadro', 'rtx', 'firepro', 'gtx 20']
        laptops_queryset = laptops_queryset.filter(Q(reduce(operator.or_, (Q(vga__icontains=x) for x in search_vga))))
        return laptops_queryset

    @classmethod
    def get_programming(cls, laptops_queryset, money_answer):
        search_cpu = ['i5', 'i7', 'i9', 'ryzen 5', 'ryzen 7', 'ryzen 9']
        search_ram = ['8GB', '16GB']
        laptops_queryset = laptops_queryset.filter(reduce(operator.or_, (Q(cpu__icontains=x) for x in search_cpu)))\
                                            .filter(reduce(operator.or_, (Q(ram__icontains=x) for x in search_ram)))\
                                            .filter(disk__icontains='ssd')
        return laptops_queryset | ExtractDataService.get_macbook(all=True, pro=True, price=money_answer)

    @classmethod
    def cluster_ai_answer(cls, content='heavy gaming'):
        ids = []
        laptops = Laptop.objects.all()
        for laptop in laptops:
            if cls.check_laptop(content, laptop):
                ids.append(laptop.id)
        laptops_queryset = laptops.filter(id__in=ids).exclude(name__icontains='macbook')
        laptops_queryset = ExtractDataService.ram_filter(laptops_queryset, min=7)

        pids = []
        for laptop in laptops_queryset:
            pids.append(laptop.id)
        answer = Answers.objects.filter(content__icontains=content).first()
        update_laptop = Laptop.objects.filter(id__in=pids)
        for laptop in update_laptop:
            purpose = laptop.purpose_group
            if str(answer.id) not in str(purpose):
                purpose = str(purpose) + '-' + str(answer.id)
                laptop.purpose_group = purpose
                laptop.save()

    @classmethod
    def distance(cls, check_laptop, train_laptop):
        laptop1_score = ClusteringScores.objects.filter(laptop=check_laptop).first()
        laptop2_score = ClusteringScores.objects.filter(laptop=train_laptop).first()
        x1 = Utils.convert_to_int(laptop1_score.detected_cpu_score)
        x2 = Utils.convert_to_int(laptop2_score.detected_cpu_score)
        y1 = Utils.convert_to_int(laptop1_score.detected_gpu_score)
        y2 = Utils.convert_to_int(laptop2_score.detected_gpu_score)
        if laptop2_score.check == 1 and x1 > x2 and y1 > y2:
            return -1  # assume very good laptop
        else:
            return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)

    @classmethod
    def check_laptop(cls, purpose, laptop):
        train_data = TrainData.objects.filter(answer_name__icontains=purpose)
        nearest = []
        for item in train_data:
            cur_laptop = item.laptop
            cal_distance = cls.distance(laptop, cur_laptop)
            if cal_distance == -1:
                return True
            if cal_distance == 0:
                return item.check
            temp = dict(check=item.check, distance=cal_distance)
            nearest.append(temp)
        nearest = sorted(nearest, key=lambda k: k['distance'])
        yes = 0
        i = 0
        while i < cls.k:
            if nearest[i]['check']:
                yes = yes + 1
            i = i + 1
        if yes > cls.k / 2:
            return True
        return False


