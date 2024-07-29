# Generated by Django 5.0.7 on 2024-07-22 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='carouselimage',
            name='author',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='carouselimage',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='內容描述'),
        ),
        migrations.AddField(
            model_name='carouselimage',
            name='title',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='標題'),
        ),
        migrations.AddField(
            model_name='carouselimage',
            name='topic',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='標籤'),
        ),
        migrations.AlterField(
            model_name='carouselimage',
            name='image',
            field=models.ImageField(upload_to='carousel/', verbose_name='輪播背景圖'),
        ),
    ]