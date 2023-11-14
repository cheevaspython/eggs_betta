from django.db import models

from general_layout.application.models import AbstractApplication
from product_eggs.models.base_client import SellerCardEggs, BuyerCardEggs
from product_eggs.models.comment import CommentEggs
from product_eggs.services.validation.validate_fields import (
    validate_c0_and_cB_count_box, validate_c1_to_dirt_count_box
)


class AbstractApplicationEggs(AbstractApplication):

    class Meta:
        abstract = True

    cB_any_color = models.BooleanField(
        editable=True, default=False,
        verbose_name='сВ цвет не важен',
    )
    c0_any_color = models.BooleanField(
        editable=True, default=False,
        verbose_name='с0 цвет не важен',
    )
    c1_any_color = models.BooleanField(
        editable=True, default=False,
        verbose_name='с1 цвет не важен',
    )
    c2_any_color = models.BooleanField(
        editable=True, default=False,
        verbose_name='с2 цвет не важен',
    )
    c3_any_color = models.BooleanField(
        editable=True, default=False,
        verbose_name='с3 цвет не важен',
    )
    cB_white = models.PositiveIntegerField(
        verbose_name='Яйца СВ белые, в десятках:',
        validators=[validate_c0_and_cB_count_box],
        default=0,
    )
    cB_white_fermer = models.BooleanField(
        editable=True, default=False,
        verbose_name='Деревенское',
    )
    cB_cream = models.PositiveIntegerField(
        verbose_name='Яйца СВ кремовые, в десятках:',
        validators=[validate_c0_and_cB_count_box],
        default=0,
    )
    cB_cream_fermer = models.BooleanField(
        editable=True, default=False,
        verbose_name='Деревенское',
    )
    cB_brown = models.PositiveIntegerField(
        verbose_name='Яйца СВ коричневые, в десятках:',
        validators=[validate_c0_and_cB_count_box],
        default=0,
    )
    cB_brown_fermer = models.BooleanField(
        editable=True, default=False,
        verbose_name='Деревенское',
    )
    c0_white = models.PositiveIntegerField(
        verbose_name='Яйца С0 белые, в десятках:',
        validators=[validate_c0_and_cB_count_box],
        default=0,
    )
    c0_white_fermer = models.BooleanField(
        editable=True, default=False,
        verbose_name='Деревенское',
    )
    c0_cream = models.PositiveIntegerField(
        verbose_name='Яйца С0 кремовые, в десятках:',
        validators=[validate_c0_and_cB_count_box],
        default=0,
    )
    c0_cream_fermer = models.BooleanField(
        editable=True, default=False,
        verbose_name='Деревенское',
    )
    c0_brown = models.PositiveIntegerField(
        verbose_name='Яйца С0 коричневые, в десятках:',
        validators=[validate_c0_and_cB_count_box],
        default=0,
    )
    c0_brown_fermer = models.BooleanField(
        editable=True, default=False,
        verbose_name='Деревенское',
    )
    c1_white = models.PositiveIntegerField(
        verbose_name='Яйца С1 белые, в десятках:',
        validators=[validate_c1_to_dirt_count_box],
        default=0,
    )
    c1_white_fermer = models.BooleanField(
        editable=True, default=False,
        verbose_name='Деревенское',
    )
    c1_cream = models.PositiveIntegerField(
        verbose_name='Яйца С1 кремовые, в десятках:',
        validators=[validate_c1_to_dirt_count_box],
        default=0,
    )
    c1_cream_fermer = models.BooleanField(
        editable=True, default=False,
        verbose_name='Деревенское',
    )
    c1_brown = models.PositiveIntegerField(
        verbose_name='Яйца С1 коричневые, в десятках:',
        validators=[validate_c1_to_dirt_count_box],
        default=0,
    )
    c1_brown_fermer = models.BooleanField(
        editable=True, default=False,
        verbose_name='Деревенское',
    )
    c2_white = models.PositiveIntegerField(
        verbose_name='Яйца С2 белые, в десятках:',
        validators=[validate_c1_to_dirt_count_box],
        default=0,
    )
    c2_cream = models.PositiveIntegerField(
        verbose_name='Яйца С2 кремовые, в десятках:',
        validators=[validate_c1_to_dirt_count_box],
        default=0,
    )
    c2_brown = models.PositiveIntegerField(
        verbose_name='Яйца С2 коричневые, в десятках:',
        validators=[validate_c1_to_dirt_count_box],
        default=0,
    )
    c3_white = models.PositiveIntegerField(
        verbose_name='Яйца С3 белые, в десятках:',
        validators=[validate_c1_to_dirt_count_box],
        default=0,
    )
    c3_cream = models.PositiveIntegerField(
        verbose_name='Яйца С3 кремовые, в десятках:',
        validators=[validate_c1_to_dirt_count_box],
        default=0,
    )
    c3_brown = models.PositiveIntegerField(
        verbose_name='Яйца С3 коричневые, в десятках:',
        validators=[validate_c1_to_dirt_count_box],
        default=0,
    )
    dirt = models.PositiveIntegerField(
        verbose_name='Грязь, в десятках:',
        validators=[validate_c1_to_dirt_count_box],
        default=0,
    )


class ApplicationFromBuyerBaseEggs(AbstractApplicationEggs):

    class Meta:
        db_table = 'ApplicationFromBuyerBaseEggs'
        verbose_name = 'Заявка от покупателя'
        verbose_name_plural = 'Заявки от покупателя'
        ordering = ['pk']

    current_buyer = models.ForeignKey(
        BuyerCardEggs, on_delete=models.PROTECT,
        verbose_name='Покупатель',
    )
    comment_json = models.OneToOneField(
        CommentEggs, on_delete=models.PROTECT,
        verbose_name='Комментарий расширенный', null=True,
        related_name='application_buyer',
    )
    cB_any_color = models.BooleanField(
        editable=True, default=False,
        verbose_name='сВ цвет не важен',
    )
    c0_any_color = models.BooleanField(
        editable=True, default=False,
        verbose_name='с0 цвет не важен',
    )
    c1_any_color = models.BooleanField(
        editable=True, default=False,
        verbose_name='с1 цвет не важен',
    )
    c2_any_color = models.BooleanField(
        editable=True, default=False,
        verbose_name='с2 цвет не важен',
    )
    c3_any_color = models.BooleanField(
        editable=True, default=False,
        verbose_name='с3 цвет не важен',
    )
    cB_white_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    cB_cream_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    cB_brown_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c0_white_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c0_cream_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c0_brown_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c1_white_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c1_cream_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c1_brown_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c2_white_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c2_cream_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c2_brown_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c3_white_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c3_cream_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c3_brown_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    dirt_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    unloading_address = models.CharField(
        max_length=255, blank=True,
        null=True, verbose_name='Адрес разгрузки',
    )
    postponement_pay = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='Отсрочка оплаты', default=0,
    )

    def __str__(self):
        return f'Заявка покупателя №{self.pk}'


class ApplicationFromSellerBaseEggs(AbstractApplicationEggs):

    class Meta:
        db_table = 'ApplicationFromSellerBaseEggs'
        verbose_name = 'Заявка от продавца'
        verbose_name_plural = 'Заявки от продавца'
        ordering = ['pk']

    current_seller = models.ForeignKey(
        SellerCardEggs, on_delete=models.PROTECT,
        verbose_name='Продавец'
    )
    comment_json = models.OneToOneField(
        CommentEggs, on_delete=models.PROTECT,
        verbose_name='Комментарий расширенный', null=True,
        related_name='application_seller',
    )
    cB_white_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    cB_cream_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    cB_brown_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c0_white_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c0_cream_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c0_brown_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c1_white_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c1_cream_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c1_brown_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c2_white_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c2_cream_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c2_brown_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c3_white_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c3_cream_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c3_brown_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    dirt_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    loading_address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Адрес погрузки',
    )
    import_application = models.BooleanField(
        editable=True, default=False, verbose_name='Импорт',
    )
    postponement_pay = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Отсрочка оплаты',
        default=0,
    )

    def __str__(self):
        return f'Заявка продавца №{self.pk}'




