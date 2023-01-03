from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User


class UserCreationFormm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'phone_number', 'full_name', 'avatar', 'is_active', 'is_admin')


class RegisterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'email-input', 'placeholder': 'ایمیل خود را وارد کنید'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'email-input', 'placeholder': 'نام کاربری خود را وارد کنید'}))
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'email-input', 'placeholder': 'نام کامل خود را وارد کنید'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'email-input', 'placeholder': 'واژهکذاره خود را وارد کنید'}), validators=[validate_password])

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError('این ایمیل قبلا ثبت شده')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError('این نام کاربری قبلا ثبت شده')
        return username



class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'email-input', 'placeholder': 'ایمیل خود را وارد کنید'})
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'email-input', 'placeholder': 'واژهکذاره خود را وارد کنید'})
    )

    def clean_password(self):
        user = authenticate(username=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        if user is not None:
            return self.cleaned_data.get('password')
        raise ValidationError('نام کاربری یا رمز ورود اشتباه است', code='invalid_info')


class EditProfileForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(
        attrs={'class': 'email-input', 'placeholder': 'پست الکترونیکی'}))

    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'email-input', 'placeholder': 'نام کاربری'}))

    full_name = forms.CharField(required=False, max_length=255, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'نام کامل'}))

    avatar = forms.ImageField(widget=forms.FileInput(attrs={"class": "d-none", "id": "select-image"}))

    def __init__(self, request, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if email != self.request.user.email:
            if user:
                raise ValidationError('این ایمیل قبلا ثبت شده')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if username != self.request.user.username:
            if user:
                raise ValidationError('این نام کاربری قبلا ثبت شده')
        return username


class CheckOTPCodeForm(forms.Form):
    code = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={'class': 'email-input', 'placeholder': 'کد تایید'}))
