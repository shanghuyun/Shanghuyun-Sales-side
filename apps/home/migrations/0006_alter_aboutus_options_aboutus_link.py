# Generated by Django 5.0.7 on 2024-07-18 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_aboutus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aboutus',
            options={'verbose_name': '關於我們', 'verbose_name_plural': '關於我們'},
        ),
        migrations.AddField(
            model_name='aboutus',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='外部連結'),
        ),
    ]