# Generated by Django 5.0.7 on 2024-07-19 11:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_mapiframe_options_alter_aboutus_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default=datetime.datetime(2024, 7, 19, 19, 20, 6, 342291), max_length=254, verbose_name='電子信箱'),
            preserve_default=False,
        ),
    ]