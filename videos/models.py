from accounts.models import Teacher, User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from utils.date_conversion.utils import jajaliConverter

# from .utils import get_total_duration_video
from django.utils.encoding import iri_to_uri


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='ادرس آی پی')

    class Meta:
        verbose_name = 'آدرس آی پی'
        verbose_name_plural = 'آدرس های آی پی'

    def __str__(self):
        return self.ip_address


class Tag(models.Model):
    name = models.CharField(max_length=155, verbose_name='نام')

    class Meta:
        verbose_name = 'تک'
        verbose_name_plural = 'تگ ها'

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=155, verbose_name='عنوان')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='parents',
                               verbose_name='')
    slug = models.SlugField(blank=True, verbose_name='اسلاگ')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Category, self).save()

    # def get_absolute_url(self):
    #     return reverse('blog:details', kwargs={'slug': self.slug})


class Video(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='videos', verbose_name='مدرس')
    title = models.CharField(max_length=255, verbose_name='عنوان')
    slug = models.SlugField(blank=True, verbose_name='اسلاگ', allow_unicode=True)
    description = models.TextField(verbose_name='توضیحات')
    cover_video = models.ImageField(upload_to='cover_video', null=True, blank=True, verbose_name='کاور ویدیو')
    video_file = models.FileField(upload_to='videos', verbose_name='فایل ویدیو')
    video_time = models.CharField(max_length=6, null=True, blank=True, verbose_name='زمان ویدیو')
    status = models.BooleanField(default=True, verbose_name='وضعیت')
    tags = models.ManyToManyField(Tag, related_name='videos', verbose_name='تگ ها')
    category = models.ManyToManyField(Category, related_name='videos', verbose_name='دسته بندی ها')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')
    updated = models.DateTimeField(auto_now=True, verbose_name='اخرین یروزرسانی')
    view = models.ManyToManyField(IPAddress, blank=True, related_name='view', verbose_name='بازدید ها')

    class Meta:
        verbose_name = 'ویدیو'
        verbose_name_plural = 'ویدیو ها'

    def __str__(self):
        return f'{self.title} - {self.teacher}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Video, self).save()

    def get_absolute_url(self):
        # url = f'{self.pk}/{self.slug}'
        # return iri_to_uri(url)
        return reverse('videos:video-detail', kwargs={'slug': self.slug})

    def jalaliPablish(self):
        return jajaliConverter(self.created)

    # def set_video_time(self):
    #     if self.video_time != '4:40':
    #         self.video_time = 'Lost'
    #         return self.video_time.save()


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', verbose_name='ویدیو')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies',
                               verbose_name='زیر مجموعه')
    text = models.TextField(verbose_name='متن')
    status = models.BooleanField(default=True, verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f'{self.user} - {self.text[:40]}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='کاربر')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes', verbose_name='ویدیو')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')

    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'

    def __str__(self):
        return f'{self.user} - {self.video.title}'


class Notification(models.Model):
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_user',
                                    verbose_name='کاربر ارسال کننده')
    geter_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='get_user',
                                   verbose_name='کاربر دریافت کننده ')
    text = models.TextField(verbose_name='متن')
    link = models.TextField(blank=True, null=True, verbose_name='لینک صفحه اعلان')
    send_email = models.BooleanField(default=False, blank=True, null=True, verbose_name='ارسال به ایمیل')

    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلان ها'

    def __str__(self):
        return self.sender_user.username
