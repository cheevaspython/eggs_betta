from django.db import models

from users.models import CustomUser


class AbstractApplication(models.Model):

    class Meta:
        abstract = True

    SHTAMP = (
        (1, 'Безликий'),
        (2, 'Подписанный'),
        (3, 'Без штампа'),
        (4, 'Любой'),
    )
    shtamp_cB_white = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп cB белые',
    )
    shtamp_cB_cream = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп cB кремовые',
    )
    shtamp_cB_brown = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп cB коричневые',
    )
    shtamp_c0_white = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c0 белые',
    )
    shtamp_c0_cream = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c0 кремовые',
    )
    shtamp_c0_brown = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c0 коричневые',
    )
    shtamp_c1_white = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c1 белые',
    )
    shtamp_c1_cream = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c1 кремовые',
    )
    shtamp_c1_brown = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c1 коричневые',
    )
    shtamp_c2_white = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c2 белые',
    )
    shtamp_c2_cream = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c2 кремовые',
    )
    shtamp_c2_brown = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c2 коричневые',
    )
    shtamp_c3_white = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c3 белые',
    )
    shtamp_c3_cream = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c3 кремовые',
    )
    shtamp_c3_brown = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп c3 коричневые',
    )
    shtamp_dirt = models.PositiveSmallIntegerField(
        choices=SHTAMP, default=1, verbose_name='Штамп грязь',
    )
    delivery_window_from = models.DateField(
        verbose_name='Окно поставки от',
        null=True, blank=True,
    )
    delivery_window_until = models.DateField(
        verbose_name='Окно поставки до',
        null=True, blank=True,
    )
    await_add_cost = models.DateField(
        verbose_name='Договорная, дата проставления цены.',
        null=True, default=None,
    )
    created_date_time = models.DateTimeField(
        auto_now_add=True, verbose_name='Создана',
    )
    edited_date_time = models.DateTimeField(
        auto_now=True, verbose_name='Изменена',
    )
    is_active = models.BooleanField(
        editable=True, default=True,
        verbose_name='Активна',
    )
    is_actual = models.BooleanField(
        editable=True, default=True,
        verbose_name='Актуальна',
    )
    owner = models.ForeignKey(
        CustomUser, verbose_name='Автор заявки',
        on_delete=models.SET_NULL, null=True,
    )
    comment = models.CharField(
        max_length=255, verbose_name='Комментарий',
        null=True, blank=True,
    )
    region = models.CharField(
        max_length=50, verbose_name='Регион',
        null=True, blank=True,
    )

