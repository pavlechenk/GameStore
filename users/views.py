from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView

from common.views import TitleMixin
from users.forms import (UserChangePasswordForm, UserLoginForm,
                         UserProfileForm, UserRegistrationForm)
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GameStore - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = "Вы успешно зарегистрировались! Вам на почту отправлено сообщения для подтверждения аккаунта."
    title = 'GameStore - Регистрация'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'GameStore - Личный Кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'GameStore - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.last().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('index'))


class UserChangePasswordView(TitleMixin, SuccessMessageMixin, FormView):
    template_name = 'users/change_password.html'
    form_class = UserChangePasswordForm
    success_message = 'Вы успешно сменили пароль!'
    title = 'GameStore - Смена пароля'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))

    def form_valid(self, form):
        current_password = form.cleaned_data.get("current_password")
        new_password1 = form.cleaned_data.get("new_password1")
        new_password2 = form.cleaned_data.get("new_password2")
        user = self.request.user

        if not user.check_password(current_password):
            form.add_error('current_password', 'Текущий пароль введен неверно')
            return self.form_invalid(form)

        if new_password1 != new_password2:
            form.add_error('new_password2', 'Новые пароли не совпадают')
            return self.form_invalid(form)

        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(self.request, user)

        return super().form_valid(form)
