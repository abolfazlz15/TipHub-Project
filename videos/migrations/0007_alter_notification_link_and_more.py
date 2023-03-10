# Generated by Django 4.1 on 2022-09-05 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='link',
            field=models.TextField(blank=True, null=True, verbose_name='لینک صفحه اعلان'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='send_all_user',
            field=models.BooleanField(default=False, verbose_name='ارسال برای همه کاربران'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='text',
            field=models.TextField(verbose_name='متن'),
        ),
    ]
