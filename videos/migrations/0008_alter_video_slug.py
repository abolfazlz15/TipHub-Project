# Generated by Django 4.1 on 2022-09-18 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_alter_notification_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, unique=True, verbose_name='اسلاگ'),
        ),
    ]