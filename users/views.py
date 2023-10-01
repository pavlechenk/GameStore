from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse_lazy
from games.models import Basket
from django.views.generic.edit import CreateView, UpdateView
from users.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'GameStore - Авторизация'
        return context


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = "Вы успешно зарегистрировались!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'GameStore - Регистрация'
        return context


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'GameStore - Личный Кабинет'
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context
