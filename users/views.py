from django.shortcuts import render, HttpResponseRedirect
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth, messages
from django.urls import reverse
from games.models import Basket
from django.contrib.auth.decorators import login_required


def login(requests):
    if requests.method == 'POST':
        form = UserLoginForm(data=requests.POST)
        if form.is_valid():
            username = requests.POST['username']
            password = requests.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(requests, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }

    return render(requests, 'users/login.html', context)


def registration(requests):
    if requests.method == 'POST':
        form = UserRegistrationForm(data=requests.POST)
        if form.is_valid():
            form.save()
            messages.success(requests, 'Вы успешно зарегестрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }

    return render(requests, 'users/registration.html', context)


@login_required
def profile(requests):
    if requests.method == 'POST':
        form = UserProfileForm(instance=requests.user, data=requests.POST, files=requests.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=requests.user)

    context = {
        'title': 'Game Store - Профиль',
        'form': form,
        'baskets': Basket.objects.filter(user=requests.user),
    }

    return render(requests, 'users/profile.html', context)


def logout(requests):
    auth.logout(requests)
    return HttpResponseRedirect(reverse('index'))
