# Generated by Django 4.1 on 2022-12-04 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0009_notification_send_email_alter_video_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='send_all_user',
        ),
    ]
