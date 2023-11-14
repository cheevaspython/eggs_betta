from django.db import models

from product_eggs.models.applications import (
    ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
)
from product_eggs.models.base_client import (
    BuyerCardEggs, LogicCardEggs, SellerCardEggs
)
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.comment import CommentEggs
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.models.entity import EntityEggs
from product_eggs.services.balance import get_cur_balance
from product_eggs.services.validation.validate_fields import (
    validate_c0_and_cB_count_box, validate_c1_to_dirt_count_box
)
from product_eggs.tasks.deal_pay_change import change_client_balance, task_calc_margin
from users.models import CustomUser


class BaseDealEggsModel(models.Model):
    """
    Основная модель, со статусами:
    просчет, подтвержденный просчет, сделка и закрытая сделка.
    каждый статус подтверждается и логируется слепок на момент перехода.
    Сделка так же имеет статусы.
    Поэтапно продвигаясь к завершению.
    """
    class Meta:
        db_table = 'BaseDealModelEggs'
        verbose_name = 'Базовая модель'
        verbose_name_plural = 'Базовые модели'
        ordering = ['pk']

    SHTAMP = (
        (1, 'Безликий'),
        (2, 'Подписанный'),
        (3, 'Без штампа'),
        (4, 'Любой'),
    )
    PAY_TYPE = ((20, 'С  НДС'), (0, 'Без НДС'))
    STATUS = (
        (1, 'Просчет'),
        (2, 'Подтвержденный просчет'),
        (3, 'Сделка'),
        (4, 'Закрытая сделка'),
    )
    STATUS_LOGIC_PAY_FORM = (
        (1, 'Оплата по форме 1, c НДС'),
        (2, 'Оплата по форме 1, без НДС'),
        (3, 'Оплата по форме 2'),
    )
    STATUS_LOGIC_PAY_TYPE = (
        (1, 'Оплата 50 / 50'),
        (2, 'Оплата по факту выгрузки'),
        (3, 'Авансовая оплата'),
    )
    DEAL_STATUS = (
        (0, 'не подтверждена'),
        (1, 'на подтверждении у фин. директора'),
        (2, 'на ожидании основания платежа от продавца'),
        (3, 'на подтверждении у фин. директора (по оплате счета от продавца'),
        (4, 'в процессе оплаты основания платежа и загрузки бухгалтером исходящего ПП'),
        (5, 'на погрузке и ожидании УПД от продавца'),
        (6, 'товар в пути, ожидаем запрос на исходящую УПД'),
        (7, 'на ожидании загрузки исходящей УПД бухгалтером'),
        (8, 'на разгрузке, ожидаем подписанную УПД'),
        (9, 'на проверке загруженных документов бухгалтером'),
        (10, 'сделка закрыта'),
    )
    # Логирование
    log_status_calc_query = models.JSONField(
        blank=True,
        default=dict, verbose_name='Лог просчета',
    )
    log_status_conf_calc_query = models.JSONField(
        blank=True,
        default=dict, verbose_name='Лог подтв. просчета',
    )
    log_status_deal_query = models.JSONField(
        blank=True,
        default=dict,
        verbose_name='Лог сделки',
    )
    log_status_edit_query = models.JSONField(
        blank=True,
        default=dict, verbose_name='Лог редактирования сделки',
    )
    # Связаные модели
    application_from_buyer = models.ForeignKey(
        ApplicationFromBuyerBaseEggs, on_delete=models.PROTECT,
        verbose_name='Заявка от покупателя',
    )
    application_from_seller = models.ForeignKey(
        ApplicationFromSellerBaseEggs, on_delete=models.PROTECT,
        verbose_name='Заявка от продавца',
    )
    buyer = models.ForeignKey(
        BuyerCardEggs, on_delete=models.PROTECT,
        verbose_name='Покупатель',
    )
    seller = models.ForeignKey(
        SellerCardEggs, on_delete=models.PROTECT,
        verbose_name='Продавец',
    )
    owner = models.ForeignKey(
        CustomUser, related_name='deal',
        verbose_name='Автор', on_delete=models.SET_NULL,
        null=True,
    )
    current_logic = models.ForeignKey(
        LogicCardEggs, on_delete=models.PROTECT,
        null=True,
        verbose_name='Перевозчик',
    )
    additional_expense = models.OneToOneField(
        AdditionalExpenseEggs, on_delete=models.PROTECT,
        verbose_name='Доп Расход', null=True,
        related_name='base_deal_model',
    )
    documents = models.OneToOneField(
        DocumentsDealEggsModel,on_delete=models.PROTECT,
        verbose_name='Документы по сделке', null=True,
        related_name='dealmodel',
    )
    comment_json = models.OneToOneField(
        CommentEggs, on_delete=models.PROTECT,
        verbose_name='Комментарий расширенный', null=True,
        related_name='base_deal',
    )
    entity = models.ForeignKey(
        EntityEggs,on_delete=models.PROTECT,
        verbose_name='Юр. лицо', null=True,
        related_name='base_deal',
    )
    # Статусы
    status = models.PositiveSmallIntegerField(
        choices=STATUS, default=1, verbose_name='Статус',
    )
    deal_status = models.PositiveSmallIntegerField(
        choices=DEAL_STATUS, default=0,
        verbose_name='Статус сделки',
    )
    delivery_form_payment = models.PositiveSmallIntegerField(
        choices=STATUS_LOGIC_PAY_FORM, default=1,
        blank=True, null=True,
        verbose_name='Статус формы оплаты логистики',
    )
    delivery_type_of_payment = models.PositiveSmallIntegerField(
        choices=STATUS_LOGIC_PAY_TYPE, default=1,
        blank=True, null=True,
        verbose_name='Статус типа оплаты логистики',
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
    # Комменты
    comment = models.TextField(
        max_length=1000, verbose_name='Комментарий',
        null=True, blank=True,
    )
    note_calc = models.TextField(
        verbose_name='Замечание к просчету',
        null=True, blank=True,
    )
    note_conf_calc = models.TextField(
        verbose_name='Замечание к подтв. просчету',
        null=True, blank=True,
    )
    # Флаги
    is_active = models.BooleanField(
        editable=True, default=True,
        verbose_name='is_active',
    )
    cash_sell = models.BooleanField(
        editable=True, default=False,
        verbose_name='Покупка за нал'
    )
    cash = models.BooleanField(
        editable=True, default=False,
        verbose_name='Продажа за нал'
    )
    import_application = models.BooleanField(
        editable=True, default=False,
        verbose_name='Импорт',
    )
    calc_to_confirm = models.BooleanField(
        editable=True, default=True,
        verbose_name='Просчет готов на подтверждение',
    )
    calc_ready = models.BooleanField(
        editable=True, default=False,
        verbose_name='Подтвержденный просчет готов',
    )
    logic_confirmed = models.BooleanField(
        editable=True, default=False,
        verbose_name='Перевозчик добавлен',
    )
    deal_status_ready_to_change = models.BooleanField(
        editable=True, default=False,
        verbose_name='Процесс смены статуса',
    )
    delivery_by_seller = models.BooleanField(
        editable=True, default=False,
        verbose_name='Доставка от продавца',
    )
    deal_status_multi = models.BooleanField(
        editable=True, default=False,
        verbose_name='Multi status deal',
    )
    # Логистика
    delivery_cost = models.FloatField(
        verbose_name='Стоимость доставки', default=0,
    )
    delivery_date_from_seller = models.DateField(
        verbose_name='Дата погрузки', null=True,
    )
    delivery_date_to_buyer = models.DateField(
        verbose_name='Дата поставки', null=True,
    )
    loading_address = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name='Адрес погрузки',
    )
    unloading_address = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name='Адрес разгрузки',
    )
    actual_loading_date = models.DateField(
        verbose_name='Фактическая дата погрузки',
        blank=True, null=True,
    )
    actual_unloading_date = models.DateField(
        verbose_name='Фактическая дата разгрузки',
        blank=True, null=True,
    )
    # Оплата
    logic_our_debt_for_app_contract = models.FloatField(
        default=0,
        verbose_name='Долг перед перевозчиком по договору-заявке',
    )
    logic_our_debt_UPD = models.FloatField(
        default=0,
        verbose_name='Долг перед перевозчиком по УПД',
    )
    #текущие суммы начинаются и заканчиваются 0. (при УПД, 0 -> рассчитались)
    logic_our_pay_amount = models.FloatField(
        default=0,
        verbose_name='Текущая сумма платежей и УПД, перевозчику по сделке',
    )
    deal_our_pay_amount = models.FloatField(
        default=0,
        verbose_name='Текущая сумма платежей и УПД, продавца по сделке',
    )
    deal_buyer_pay_amount = models.FloatField(
        default=0,
        verbose_name='Текущая сумма платежей и УПД, покупателя по сделке',
    )
    payback_day_for_us = models.DateField(
        verbose_name='Дата оплаты для нас',
        null=True, blank=True,
    )
    payback_day_for_us_logic = models.DateField(
        verbose_name='Дата оплаты для нас перевозчику',
        null=True, blank=True,
    )
    payback_day_for_buyer = models.DateField(
        verbose_name='Дата оплаты для покупателя',
        null=True, blank=True,
    )
    postponement_pay_for_us = models.PositiveIntegerField(
        default=0, verbose_name='Отсрочка оплаты для нас'
    )
    postponement_pay_for_buyer = models.PositiveIntegerField(
        default=0, verbose_name='Отсрочка оплаты для покупателя'
    )
    deal_our_debt_UPD = models.FloatField(
        default=0,
        verbose_name='Долг перед продавцом по сделке по УПД',
    )
    deal_buyer_debt_UPD = models.FloatField(
        default=0,
        verbose_name='Долг перед нами по сделке по УПД',
    )
    margin = models.FloatField(
        default=0,
        verbose_name='Маржа',
    )
    # Товар
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
    seller_cB_white_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_cB_cream_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_cB_brown_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c0_white_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c0_cream_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c0_brown_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c1_white_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c1_cream_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c1_brown_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c2_white_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c2_cream_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c2_brown_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c3_white_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c3_cream_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c3_brown_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_dirt_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    buyer_cB_white_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_cB_cream_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_cB_brown_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c0_white_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c0_cream_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c0_brown_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c1_white_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c1_cream_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c1_brown_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c2_white_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c2_cream_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c2_brown_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c3_white_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c3_cream_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c3_brown_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_dirt_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__deal_buyer_pay_amount = self.deal_buyer_pay_amount
        self.__deal_our_pay_amount = self.deal_our_pay_amount
        self.__logic_our_pay_amount = self.logic_our_pay_amount

    def save(self, *args, **kwargs):
        self.deal_buyer_pay_amount = round(self.deal_buyer_pay_amount, 2)
        self.deal_our_pay_amount = round(self.deal_our_pay_amount, 2)
        self.logic_our_pay_amount = round(self.logic_our_pay_amount, 2)
        self.margin = task_calc_margin(self)
        super(BaseDealEggsModel, self).save(*args, **kwargs)

        creating = not bool(self.pk)
        if creating:
            pass
        else:
            if self.deal_our_pay_amount != self.__deal_our_pay_amount:
                if self.entity:
                    delta = self.deal_our_pay_amount - self.__deal_our_pay_amount
                    balance = get_cur_balance(self.entity, self.seller)
                    change_client_balance(balance, delta, self.cash)
                else:
                    raise KeyError(f'error in basedeal -> {self.pk} deal_pays changed, but self entity is None!!!')

            if self.deal_buyer_pay_amount != self.__deal_buyer_pay_amount:
                if self.entity:
                    delta = self.deal_buyer_pay_amount - self.__deal_buyer_pay_amount
                    balance = get_cur_balance(self.entity, self.buyer)
                    change_client_balance(balance, delta, self.cash)
                else:
                    raise KeyError(f'error in basedeal -> {self.pk} deal_pays changed, but self entity is None!!!')

            if self.logic_our_pay_amount != self.__logic_our_pay_amount:
                if self.current_logic and self.entity:
                    delta = self.logic_our_pay_amount - self.__logic_our_pay_amount
                    balance = get_cur_balance(self.entity, self.current_logic)
                    if self.delivery_form_payment == 3:
                        change_client_balance(balance, delta, True)
                    else:
                        change_client_balance(balance, delta, False)
                else:
                    raise KeyError(f'error in basedeal -> {self.pk} logic_pay changed, but self current_logic is None or entity is None!!!')


    def __str__(self):
        if self.status == 1:
            return f'Просчет №{self.pk}'
        elif self.status == 2:
            return f'Подтвержденный просчет №{self.pk}'
        elif self.status == 3:
            return f'Сделка №{self.pk}'
        elif self.status == 4:
            return f'Закрытая сделка №{self.pk}'





