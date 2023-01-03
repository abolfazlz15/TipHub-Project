from django.apps import AppConfig


class VideosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videos'
    verbose_name = 'ویدیو ها'

    def ready(self):
        import videos.signals