# Generated by Django 3.0.5 on 2020-04-28 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cart_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='category',
            field=models.CharField(default=' ', max_length=200),
        ),
    ]
