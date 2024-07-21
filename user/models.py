from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from user import utils


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, login, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not login:
            raise ValueError('User must have an Email or Phone')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password):
        """create a superuser"""
        user = self.create_user(login, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def clean(self):
        self.set_password(self.password)


class User(AbstractBaseUser, PermissionsMixin):
    """Model for user"""
    name = models.CharField(max_length=200, verbose_name="ФИО")
    phone = models.CharField("Номер телефона", max_length=200, null=True, blank=True)
    user_type = models.CharField("Тип пользователя", max_length=50, choices=utils.USER_TYPE, default=utils.ADMINISTRATOR)
    login = models.CharField(max_length=200, unique=True, verbose_name="Логин")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    status = models.CharField('Статус', max_length=20, choices=utils.USER_STATUS, default=utils.ACTIVE)

    objects = UserManager()

    USERNAME_FIELD = 'login'
