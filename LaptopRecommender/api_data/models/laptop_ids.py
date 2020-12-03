from django.db import models


class LaptopId(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.CharField(max_length=255, default='')
    thumbnails = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'laptop_id'

