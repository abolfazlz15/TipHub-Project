from random import randint

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, TemplateView, View

from .forms import CheckOTPCodeForm, EditProfileForm, LoginForm, RegisterForm
from .models import OTPCode, User


class EditUserPanelView(LoginRequiredMixin, View):
    template_name = "accounts/edit-user-panel.html"
    form_class = EditProfileForm

    def get_form_kwargs(self):
        kwargs = super(EditUserPanelView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request):
        form = self.form_class(request, initial={
            'email': request.user.email,
            'username': request.user.username,
            'phone_number': request.user.phone_number,
            'full_name': request.user.full_name,
            'avatar': request.user.avatar,
        })
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        old_email = request.user.email,
        form = self.form_class(request, request.POST, request.FILES,
                               initial={
                                   'email': request.user.email,
                                   'username': request.user.username,
                                   'phone_number': request.user.phone_number,
                                   'full_name': request.user.full_name,
                                   'avatar': request.user.avatar,
                               })

        if form.is_valid():
            global data
            data = form.cleaned_data
            request.user.username = data['username']
            request.user.full_name = data['full_name']
            request.user.avatar = data['avatar']
            old_email = ''.join(map(str, list(old_email)))

            if data['email'] != old_email:
                random_code = randint(1000, 9999)
                OTPCode.objects.create(email=data['email'], code=random_code)

                mail_subject = 'فعال سازی اکانت'
                message = render_to_string('accounts/active_email.html', {
                    'user': data['username'],
                    'code': random_code,
                })
                to_email = data['email']
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return redirect('accounts:check-email-otp')
            request.user.save()
            return redirect('accounts:user-panel')
        return render(request, self.template_name, {'form': form})


class CheckOTPCodeEmailChangeView(View):
    form_class = CheckOTPCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/check_otp.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data
            try:

                otp = OTPCode.objects.get(code=code['code'], email=data['email'])
                expiration_date = otp.expiration_date + timezone.timedelta(minutes=2)
                if expiration_date < timezone.now():
                    otp.delete()
                    messages.add_message(request, messages.WARNING, 'زمان اعتبار کد تایید شما تمام شده')
                    return render(request, 'accounts/check_otp.html', {'form': form})

                elif OTPCode.objects.filter(code=code['code'], email=data['email']).exists():
                    user = User.objects.get(id=request.user.id)
                    user.email = data['email']
                    user.save()
                    otp.delete()
                    return redirect('videos:home')
            except:
                messages.add_message(request, messages.ERROR, 'Your code is not valid')
                return render(request, 'accounts/check_otp.html', {'form': form})


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        randcode = randint(1000, 9999)
        data = form.cleaned_data
        OTPCode.objects.create(email=data['email'], code=randcode)
        self.request.session['user_info'] = {
            'email': data['email'],
            'username': data['username'],
            'full_name': data['full_name'],
            'password': data['password'],
        }

        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('accounts/active_email.html', {
            'user': data['username'],
            'code': randcode,
        })
        to_email = data['email']
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return redirect('accounts:check-otp')


class CheckOTPCodeView(View):
    form_class = CheckOTPCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/check_otp.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        user_session = request.session['user_info']
        if form.is_valid():
            data = form.cleaned_data
            try:
                otp = OTPCode.objects.get(code=data['code'], email=user_session['email'])
                expiration_date = otp.expiration_date + timezone.timedelta(minutes=2)

                if expiration_date < timezone.now():
                    otp.delete()
                    messages.add_message(request, messages.WARNING, 'زمان اعتبار کد تایید شما تمام شده')
                    return render(request, 'accounts/check_otp.html', {'form': form})

                elif OTPCode.objects.filter(code=data['code'], email=user_session['email']).exists():
                    user = User.objects.create(email=otp.email, username=user_session['username'],
                                               full_name=user_session['full_name'], password=user_session['password'])
                    user.set_password(user_session['password'])
                    user.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    otp.delete()
                    return redirect('videos:home')
            except:
                messages.add_message(request, messages.ERROR, 'کد تایید شما معتبر نمیباشد')
                return render(request, 'accounts/check_otp.html', {'form': form})


class LoginView(View):
    form_class = LoginForm
    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(email=data['email'])
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')

        return render(request, "accounts/login.html", {"form": form})

    def get(self, request):


        form = self.form_class()

        return render(request, "accounts/login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')


class UserPanelView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user-panel.html'
