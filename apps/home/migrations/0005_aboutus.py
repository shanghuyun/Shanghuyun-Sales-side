# Generated by Django 5.0.7 on 2024-07-18 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_carouselimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=10, null=True, verbose_name='標題')),
                ('simple_introduce', models.CharField(blank=True, max_length=100, null=True, verbose_name='簡單介紹')),
                ('introduce', models.TextField(blank=True, null=True, verbose_name='完整介紹')),
                ('image', models.ImageField(upload_to='Aboutus')),
            ],
        ),
    ]