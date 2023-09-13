from django.shortcuts import render


def login(requests):
    return render(requests, 'users/login.html')


def registration(requests):
    return render(requests, 'users/registration.html')
