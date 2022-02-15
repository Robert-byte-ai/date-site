from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import add_watermark

GENDER = [
    ('male', 'male'),
    ('female', 'female'),
]


class User(AbstractUser):
    first_name = models.CharField(
        max_length=40,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=40,
        blank=False,
        verbose_name='Фамилия'
    )
    gender = models.CharField(
        max_length=40,
        choices=GENDER,
        verbose_name='Пол',
    )
    email = models.EmailField(
        max_length=60,
        blank=False,
        unique=True,
        verbose_name='Электронная почта'
    )
    avatar = models.ImageField(
        upload_to='users_avatars',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    latitude = models.DecimalField(
        decimal_places=16,
        max_digits=22,
        verbose_name='Широта',
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        decimal_places=16,
        max_digits=22,
        verbose_name='Долгота',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-pk',)

    def save(self, *args, **kwargs):
        super().save()
        if self.avatar:
            add_watermark(self.avatar.path)

    def __str__(self):
        return self.username


class Match(models.Model):
    user = models.ForeignKey(
        User,
        related_name='who_liked',
        on_delete=models.CASCADE
    )

    liked_user = models.ForeignKey(
        User,
        related_name='liked_user',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('-id',)
