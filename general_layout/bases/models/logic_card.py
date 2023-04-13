from django.db import models


class LogicCard(models.Model):
    PAY_TYPE = ((20, 'С  НДС'), (0, 'Без НДС'))

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=50, null=True, 
        blank=True, verbose_name='Название перевозчика'
    )
    inn = models.CharField(
        max_length=20, blank=True, 
        null=True, verbose_name='ИНН логиста'
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
    pay_type = models.PositiveSmallIntegerField(
        'Тип оплаты', choices=PAY_TYPE, 
        null=True, blank=True
    )
    comment = models.CharField(
        max_length=255, blank=True, null=True, 
        verbose_name='Дополнительная информация'
    )
    # rating = None

    def __str__(self):
        return f'{self.name}, {self.inn}'
