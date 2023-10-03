from django.urls import path
from users.views import UserLoginView, UserRegistrationView, UserProfileView, UserChangePasswordView, EmailVerificationView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('change_password/', login_required(UserChangePasswordView.as_view()), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='email_verification'),
]
