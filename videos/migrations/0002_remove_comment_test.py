# Generated by Django 4.1 on 2022-08-26 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='test',
        ),
    ]
