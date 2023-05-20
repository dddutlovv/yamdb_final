from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self,
                    username,
                    email,
                    password,
                    bio,
                    role,
                    **extra_fields):
        if not username:
            raise ValueError(("Поле username должно быть заполнено"))
        if not email:
            raise ValueError(("Поле email должно быть заполнено"))
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          password=password,
                          bio=bio,
                          role=role,
                          **extra_fields)
        user.save()
        return user

    def create_superuser(self,
                         username,
                         email,
                         password,
                         bio,
                         role,
                         **extra_fields):
        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                bio=bio,
                                role=role,
                                **extra_fields)
        user.role = 'admin'
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    ROLES = [
        ('user', 'user'),
        ('admin', 'admin'),
        ('moderator', 'moderator'),
    ]

    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.TextField(
        verbose_name='Роль',
        choices=ROLES,
        default='user'
    )
    password = models.CharField(
        max_length=150,
        blank=True
    )

    # objects = UserManager()

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ['id']
