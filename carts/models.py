from datetime import datetime

from django.db import models


class Cart(models.Model):
    product = models.CharField(max_length=200)
    product_id = models.IntegerField()
    product_price = models.IntegerField()
    user_id = models.IntegerField()
    cart_date = models.DateTimeField(default=datetime.now, blank=True)
    quantity = models.IntegerField(default=1)
    category = models.CharField(max_length=200,default=" ")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=" ")
    is_published = models.BooleanField(default=True)


    def get_total_item_price(self):
        return self.quantity * self.product_price
