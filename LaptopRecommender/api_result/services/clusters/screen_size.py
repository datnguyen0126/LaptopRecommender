

class ScreenSizeCluster:

    @classmethod
    def screen_size_cluster(cls, answer):
        pass

    @classmethod
    def get_value(cls, screen_sizes):
        ret = []
        for size in screen_sizes:
            temp = ''
            if '13' in size:
                temp = '13'
            if '14' in size:
                temp = '14'
            if '15' in size:
                temp = '15'
            if '17' in size:
                temp = '17'
            ret.append(temp)
        return ret