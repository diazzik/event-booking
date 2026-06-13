from django.contrib.auth.models import AbstractUser
from django.db import models
from events.models import Event

class User(AbstractUser):

    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('admin', 'Администратор')
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    
    favorites = models.ManyToManyField(
        Event,
        blank=True,
        related_name='favorited_by'
    )
    
    def __str__(self):
        return self.username