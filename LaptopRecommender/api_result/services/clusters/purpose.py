from api_data.models import Laptop
from api.utils import Utils
from api_result.models import ClusteringScores, TrainData


class PurposeCluster:
    k = 7
    options = [
        "Web browsing",
        "Social Media",
        "Email",
        "Document",
        "Watching Movies",
        "Light Gaming",
        "Heavy Gaming",
        "Photo editing (basic)",
        "Photo editing (pro)",
        "Video production basic)",
        "Video production (pro)",
        "3D design",
        "Science study"
        "Front-end developer",
        "Back-end developer"
    ]

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
    def cluster_purpose(cls, laptops, purpose_answer):
        answers = cls.get_answer_index(purpose_answer)
        if answers.get(0):
            laptops = cls.get_Web_browsing(laptops)
        if answers.get(1):
            laptops = cls.get_Social_media(laptops)
        if answers.get(2):
            laptops = cls.get_Email(laptops)
        if answers.get(3):
            laptops = cls.get_Document(laptops)
        if answers.get(4):
            laptops = cls.get_Watching_Movies(laptops)
        if answers.get(5):
            laptops = cls.get_Light_Gaming(laptops)
        if answers.get(6):
            laptops = cls.get_Heavy_Gaming(laptops)
        if answers.get(7):
            laptops = cls.get_Photo_editing_basic(laptops)
        if answers.get(8):
            laptops = cls.get_Photo_editing_pro(laptops)
        if answers.get(9):
            laptops = cls.get_Video_production_basic(laptops)
        if answers.get(10):
            laptops = cls.get_Video_production_pro(laptops)
        if answers.get(11):
            laptops = cls.get_3D_design(laptops)
        if answers.get(12):
            laptops = cls.get_Science_study(laptops)
        if answers.get(13):
            laptops = cls.get_Frontend_developer(laptops)
        if answers.get(14):
            laptops = cls.get_Backend_developer(laptops)
        return laptops

    @classmethod
    def get_Web_browsing(cls, laptops_queryset):
        return laptops_queryset

    @classmethod
    def get_Email(cls, laptops_queryset):
        return laptops_queryset

    @classmethod
    def get_Social_media(cls, laptops_queryset):
        return laptops_queryset

    @classmethod
    def get_Document(cls, laptops_queryset):
        return laptops_queryset

    @classmethod
    def get_Watching_Movies(cls, laptops_queryset):
        # laptops_queryset = laptops_queryset.filter()
        return laptops_queryset

    @classmethod
    def get_Light_Gaming(cls, laptops_queryset):
        temp_laptops = laptops_queryset.copy()
        ids = [laptop.id for laptop in laptops_queryset if cls.check_laptop('light gaming', laptop)]
        temp_laptops = temp_laptops(id__in=ids)
        return temp_laptops

    @classmethod
    def get_Heavy_Gaming(cls, laptops_queryset):
        ids = []
        for laptop in laptops_queryset:
            if cls.check_laptop('Heavy gaming', laptop):
                print(1)
                ids.append(laptop.id)
        laptops_queryset = laptops_queryset.filter(id__in=ids)
        return laptops_queryset

    @classmethod
    def get_Photo_editing_pro(cls, laptops_queryset):
        temp_laptops = laptops_queryset.copy()
        ids = [laptop.id for laptop in laptops_queryset if cls.check_laptop('Photo editing (pro)', laptop)]
        temp_laptops = temp_laptops(id__in=ids)
        return temp_laptops

    @classmethod
    def get_Photo_editing_basic(cls, laptops_queryset):
        temp_laptops = laptops_queryset.copy()
        ids = [laptop.id for laptop in laptops_queryset if cls.check_laptop('Photo editing (basic)', laptop)]
        temp_laptops = temp_laptops(id__in=ids)
        return temp_laptops

    @classmethod
    def get_Video_production_pro(cls, laptops_queryset):
        temp_laptops = laptops_queryset.copy()
        ids = [laptop.id for laptop in laptops_queryset if cls.check_laptop('Video production (pro)', laptop)]
        temp_laptops = temp_laptops(id__in=ids)
        return temp_laptops

    @classmethod
    def get_Video_production_basic(cls, laptops_queryset):
        temp_laptops = laptops_queryset.copy()
        ids = [laptop.id for laptop in laptops_queryset if cls.check_laptop('Video production basic)', laptop)]
        temp_laptops = temp_laptops(id__in=ids)
        return temp_laptops

    @classmethod
    def get_3D_design(cls, laptops_queryset):
        laptops_queryset = laptops_queryset.filter(vga__icontains='quadro')
        return laptops_queryset

    @classmethod
    def get_Science_study(cls, laptops_queryset):
        temp_laptops = laptops_queryset.copy()
        ids = [laptop.id for laptop in laptops_queryset if cls.check_laptop('Science study', laptop)]
        temp_laptops = temp_laptops(id__in=ids)
        return temp_laptops

    @classmethod
    def get_Frontend_developer(cls, laptops_queryset):
        temp_laptops = laptops_queryset.copy()
        ids = [laptop.id for laptop in laptops_queryset if cls.check_laptop('Front-end developer', laptop)]
        temp_laptops = temp_laptops(id__in=ids)
        return temp_laptops

    @classmethod
    def get_Backend_developer(cls, laptops_queryset):
        temp_laptops = laptops_queryset.copy()
        ids = [laptop.id for laptop in laptops_queryset if cls.check_laptop('Back-end developer', laptop)]
        temp_laptops = temp_laptops(id__in=ids)
        return temp_laptops

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


