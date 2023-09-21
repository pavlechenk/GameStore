from django.shortcuts import render, HttpResponseRedirect
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth
from django.urls import reverse


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
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }

    return render(requests, 'users/registration.html', context)


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
        'form': form
    }

    return render(requests, 'users/profile.html', context)
