from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView

from common.views import TitleMixin
from users.forms import (UserChangePasswordForm, UserEmailForgotPasswordForm,
                         UserLoginForm, UserProfileForm, UserRegistrationForm,
                         UserResetPasswordForm)
from users.models import EmailResetPassword, EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GameStore - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    title = 'GameStore - Регистрация'

    def get_success_message(self, cleaned_data):
        user = User.objects.get(id=self.object.id)
        return f"Вы успешно зарегистрировались! На почту {user.email}" \
               " отправлено сообщения для подтверждения аккаунта."


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'GameStore - Личный Кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'GameStore - Подтверждение электронной почты'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.last().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('index'))


class PasswordResetSuccessfullyView(TitleMixin, TemplateView):
    template_name = 'users/password_reset_successfully.html'
    title = 'GameStore - Пароль успешно сброшен'


class UserResetPasswordView(TitleMixin, FormView):
    form_class = UserResetPasswordForm
    success_url = reverse_lazy('users:password_reset_successfully')
    template_name = 'users/reset_password.html'
    title = 'GameStore - Сброс пароля'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.kwargs.get('email')
        context['code'] = self.kwargs.get('code')
        return context

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_reset_password = EmailResetPassword.objects.filter(user=user, code=code).first()
        if email_reset_password and not email_reset_password.is_expired():
            return super().get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('index'))

    def form_valid(self, form):
        email = self.kwargs.get('email')
        code = self.kwargs.get('code')
        form.save(self.request, email, code)

        return super().form_valid(form)


class UserForgotPasswordView(TitleMixin, SuccessMessageMixin, FormView):
    form_class = UserEmailForgotPasswordForm
    template_name = 'users/forgot_password.html'
    success_url = reverse_lazy('users:login')
    title = 'GameStore - Сброс пароля'

    def get_success_message(self, cleaned_data):
        return f'Сообщение было успешно отправлено на почту {cleaned_data.get("email")}'

    def form_valid(self, form):
        return super().form_valid(form)


class UserChangePasswordView(TitleMixin, SuccessMessageMixin, FormView):
    form_class = UserChangePasswordForm
    success_message = 'Вы успешно сменили пароль!'
    template_name = 'users/change_password.html'
    title = 'GameStore - Смена пароля'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))

    def form_valid(self, form):
        current_password = form.cleaned_data.get("current_password")
        new_password1 = form.cleaned_data.get("new_password1")
        new_password2 = form.cleaned_data.get("new_password2")
        user = self.request.user

        if not user.check_password(current_password):
            form.add_error("current_password", "Текущий пароль введен неверно")
            return self.form_invalid(form)

        if new_password1 != new_password2:
            form.add_error("new_password2", "Новые пароли не совпадают")
            return self.form_invalid(form)

        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(self.request, user)

        return super().form_valid(form)
