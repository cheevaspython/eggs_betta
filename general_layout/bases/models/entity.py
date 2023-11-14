from django.db import models
from django.core import validators


class Entity(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название',
    )
    inn = models.CharField(
        max_length=12,
        verbose_name='ИНН',
        validators=[
            validators.MaxLengthValidator(12),
            validators.MinLengthValidator(10)
        ],
        primary_key=True,
    )
