from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    email = models.EmailField(unique=True)
    is_verified_email = models.BooleanField(default=False)


class BaseEmailSending(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __init__(self, subject, message):
        super().__init__()
        self.subject = subject
        self.message = message

    def send_email(self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False

    def _get_full_link(self, view_name):
        url = reverse(view_name, args=(self.user.email, self.code))
        full_link = f"{settings.DOMAIN_NAME}{url}"
        return full_link


class EmailVerification(BaseEmailSending):
    def __init__(self):
        subject = f"Подтверждение учетной записи для {self.user.username}"
        message = "Для подтверждения учетной записи для {} перейдите по ссылке {}".format(
            self.user.email, self._get_full_link('users:email_verification')
        )
        super().__init__(subject, message)

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"


class EmailResetPassword(BaseEmailSending):

    def __init__(self):
        subject = f"Сброс пароля учетной записи {self.user.username}"
        message = "Для сброса пароля учетной записи {} перейдите по ссылке {}".format(
            self.user.email, self._get_full_link('users:reset_password')
        )
        super().__init__(subject, message)

    def __str__(self):
        return f"EmailResetPassword object for {self.user.email}"
