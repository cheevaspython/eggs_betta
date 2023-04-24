from django.core import validators
from django.db import models


class LogicCard(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=255, unique=True, verbose_name='Название', 
    )
    inn = models.CharField(
        max_length=12, verbose_name='ИНН / Паспорт',   
        validators=[validators.MaxLengthValidator(12),
            validators.MinLengthValidator(10)],
        primary_key=True,
    )
    general_manager = models.CharField(
        max_length=255, blank=True, 
        null=True, verbose_name='Генеральный директор'
    )
    contact_person = models.CharField(
        max_length=255, blank=True, 
        null=True, verbose_name='Контактное лицо'
    )
    phone = models.CharField(
        max_length=50, blank=True, 
        null=True, verbose_name='Контактный номер'
    )
    email = models.EmailField(
        max_length=50, blank=True, 
        null=True, verbose_name='Почта'
    )
    comment = models.CharField(
        max_length=255, blank=True, null=True, 
        verbose_name='Дополнительная информация'
    )
    # rating = None

    def __str__(self):
        return f'{self.name}, {self.inn}'
