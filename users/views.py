from django.shortcuts import render, HttpResponseRedirect
from users.forms import UserLoginForm
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

    context = {
        'form': UserLoginForm(),
    }

    return render(requests, 'users/login.html', context)


def registration(requests):
    return render(requests, 'users/registration.html')
