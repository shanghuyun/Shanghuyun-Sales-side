# Generated by Django 5.0.7 on 2024-07-18 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_webbasicinf_alter_profile_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='carousel/', verbose_name='輪播圖')),
            ],
            options={
                'verbose_name': '輪播圖',
                'verbose_name_plural': '輪播圖',
            },
        ),
    ]
