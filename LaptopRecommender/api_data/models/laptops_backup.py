from django.db import models


class LaptopBackup(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(default=0, blank=True, null=True)
    stock = models.IntegerField(default=0, blank=True, null=True)
    rating_average = models.CharField(max_length=255, blank=True, null=True)
    review_count = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    dimension = models.TextField(blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    cpu = models.CharField(max_length=255, blank=True, null=True)
    display = models.CharField(max_length=255, blank=True, null=True)
    screen_size = models.CharField(max_length=255, blank=True, null=True)
    vga = models.CharField(max_length=255, blank=True, null=True)
    disk = models.CharField(max_length=255, blank=True, null=True)
    ram = models.CharField(max_length=255, blank=True, null=True)
    battery = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'laptop_backup'


