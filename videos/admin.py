from django.contrib import admin

from . import models

admin.site.register(models.Video)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.Like)
admin.site.register(models.IPAddress)
admin.site.register(models.Notification)