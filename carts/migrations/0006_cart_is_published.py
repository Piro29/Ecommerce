# Generated by Django 3.0.5 on 2021-04-18 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_cart_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]
