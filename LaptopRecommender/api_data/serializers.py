from rest_framework import serializers
from api_data.models import Laptop, LaptopId


class LaptopSerializers(serializers.ModelSerializer):

    class Meta:
        model = Laptop
        fields = '__all__'
        extra_kwargs = {
            'id': { 'required': False }
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        laptop_id = LaptopId.objects.filter(id=ret.get('id')).first()
        if laptop_id:
            ret.update(link=laptop_id.link)
            ret.update(thumbnails=laptop_id.thumbnails)
        return ret

