from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.path = reverse('users:login')

    def test_user_login_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'GameStore - Авторизация')
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_login_post(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

    def test_user_login_error(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.data = {
            'first_name': 'Александр',
            'last_name': 'Раздымахо',
            'username': 'pavlechenk',
            'email': 'pavlechenk@gmail.com',
            'password1': 'A888rz08',
            'password2': 'A888rz08',
        }

        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'GameStore - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email_verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_error(self):
        User.objects.create(username=self.data['username'], email=self.data['email'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
        self.assertContains(response, 'Пользователь с таким Email уже существует.', html=True)
