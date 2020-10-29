from rest_framework import serializers
from api_result.models import ClusteringScores, TrainData
from api_data.serializers import LaptopSerializers


class ClusterScoreSerializers(serializers.ModelSerializer):

    class Meta:
        model = ClusteringScores
        fields = '__all__'


class ClusterQuestionSerializers(serializers.ModelSerializer):

    class Meta:
        model = TrainData
        fields = '__all__'
