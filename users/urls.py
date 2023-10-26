from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (EmailVerificationView, PasswordResetSuccessfullyView,
                         UserChangePasswordView, UserForgotPasswordView,
                         UserLoginView, UserProfileView, UserRegistrationView,
                         UserResetPasswordView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('change_password/', login_required(UserChangePasswordView.as_view()), name='change_password'),
    path('reset_password/<str:email>/<uuid:code>', UserResetPasswordView.as_view(), name='reset_password'),
    path('password_reset_successfully/', PasswordResetSuccessfullyView.as_view(), name='password_reset_successfully'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='email_verification'),
    path('forgot_password/', UserForgotPasswordView.as_view(), name='forgot_password'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
]
