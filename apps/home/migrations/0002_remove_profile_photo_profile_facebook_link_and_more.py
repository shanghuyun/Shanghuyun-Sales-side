# Generated by Django 5.0.7 on 2024-07-18 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='photo',
        ),
        migrations.AddField(
            model_name='profile',
            name='facebook_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='youtube_link',
            field=models.URLField(blank=True),
        ),
    ]