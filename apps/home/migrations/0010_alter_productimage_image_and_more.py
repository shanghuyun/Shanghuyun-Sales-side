# Generated by Django 5.0.7 on 2024-07-18 10:03

import apps.home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_aboutus_options_alter_carouselimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=apps.home.models.get_product_image_upload_path, verbose_name='商品照片'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='cover_image',
            field=models.ImageField(upload_to=apps.home.models.get_product_cover_image_upload_path, verbose_name='商品封面圖片'),
        ),
    ]