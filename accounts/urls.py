from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('check-otp/', views.CheckOTPCodeView.as_view(), name='check-otp'),
    path('check-email-otp/', views.CheckOTPCodeEmailChangeView.as_view(), name='check-email-otp'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user/', views.UserPanelView.as_view(), name='user-panel'),
    path('user/edit', views.EditUserPanelView.as_view(), name='edit-user-panel')
]

# rest password URL
urlpatterns += [
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html', success_url=reverse_lazy('accounts:password_change_done')), name='change-password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),
         name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset.html'),
        name="password_reset_complete",
    ),
]
