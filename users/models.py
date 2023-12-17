from django.db import models
from django.contrib.auth.models import AbstractUser

from product_eggs.models.entity import EntityEggs


class Role(models.TextChoices):
    manager_sell = '1', 'менеджер продажа'
    manager_buy = '2', 'менеджер покупка'
    manager_sell_and_buy = '3', 'менеджер покупка продажа'
    logic = '4', 'логист'
    manager_way = '5', 'менеджер направления'
    money_manager = '6', 'фин директор'
    accountant = '7', 'бухгалтер'
    super_user = '8', 'cупер юзер'
    manager_admin = '9', 'менеджер администратор'
    guest = '10', 'Гость'


class CustomUser(AbstractUser):
    role = models.CharField(
        verbose_name='роль', max_length=25,
        choices=Role.choices, default=Role.manager_sell
    )
    phone_number = models.CharField(
        max_length=20, null=True,
        blank=True, verbose_name='телефон'
    )
    master_password = models.CharField(
        max_length=30, null=True,
        blank=True, verbose_name='Мастер пароль'
    )
    def __str__(self):
        return self.username


# class UserPermissionClass(models.TextChoices):
    ...







