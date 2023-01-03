from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.html import format_html

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='پست الکترونیکی',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=155, unique=True, verbose_name='نام کاربری')
    full_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='نام کامل')
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name='شماره همراه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    avatar = models.ImageField(upload_to='avatar_user', null=True, blank=True, verbose_name='عکس پروفایل')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):

        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):

        return self.is_admin

    def showImage(self):
        if self.avatar:
            return format_html(f'<img src="{self.avatar.url}" alt="" width="50px" height="50px">')
        else:
            return format_html('پروفایل ندارد')

    showImage.short_description = 'عکس پروفایل'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_rel', verbose_name=' کاربر')
    bio = models.TextField(verbose_name='بیو')
    twitter = models.URLField(null=True, blank=True, verbose_name='توییتر')
    linkedin = models.URLField(null=True, blank=True, verbose_name='لینکدین')
    github = models.URLField(null=True, blank=True, verbose_name='گیت هاب')
    instagram = models.URLField(null=True, blank=True, verbose_name='اینستاگرام')

    class Meta:
        verbose_name = 'معلم'
        verbose_name_plural = 'معلمین'

    def __str__(self):
        return self.user.username


class OTPCode(models.Model):
    email = models.CharField(max_length=200)
    code = models.SmallIntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
