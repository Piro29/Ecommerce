from django.db import models
from datetime import datetime
from django.contrib.auth.models import Group


class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, default='Both')
    size = models.CharField(max_length=4)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title
