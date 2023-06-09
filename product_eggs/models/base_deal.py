from django.db import models
        
from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
    ApplicationFromSellerBaseEggs
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, \
    SellerCardEggs
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.services.base_deal.margin import calculate_margin
from product_eggs.tasks.deal_pay_change import change_client_balance_deal
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
        (4, 'на ожидании оплаты и загрузки бухгалтером исходящего ПП'),
        (5, 'на погрузке и ожидании УПД от продавца'),
        (6, 'товар в пути, ожидаем запрос на исходящую УПД'),
        (7, 'на ожидании загрузки исходящей УПД бухгалтером'),
        (8, 'на разгрузке, ожидаем подписанную УПД'),
        (9, 'на ожидании закрывающих документов'),
    )
    # Логирование
    log_status_calc_query = models.JSONField(
        blank=True, null=True,
        default=dict, verbose_name='Лог просчета',
    )
    log_status_conf_calc_query = models.JSONField(
        blank=True, null=True,
        default=dict, verbose_name='Лог подтв. просчета',
    )
    log_status_deal_query = models.JSONField(
        blank=True, null=True,
        default=dict,
        verbose_name='Лог сделки перед завершением',
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
        verbose_name='Логист',
    )
    additional_expense = models.OneToOneField(
        AdditionalExpenseEggs, on_delete=models.PROTECT, 
        verbose_name='Доп Расход', null=True,
    )
    documents = models.OneToOneField(
        DocumentsDealEggsModel,on_delete=models.PROTECT, 
        verbose_name='Документы по сделке', null=True,
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
    cash = models.BooleanField(
        editable=True, default=False,
        verbose_name='Продажа за нал'
    )
    import_application = models.BooleanField(
        editable=True, default=False,
        verbose_name='Импорт',
    )
    calc_ready = models.BooleanField(
        editable=True, default=False,
        verbose_name='Просчет готов',
    )
    logic_confirmed = models.BooleanField(
        editable=True, default=False,
        verbose_name='Логист добавлен',
    )
    deal_status_ready_to_change = models.BooleanField(
        editable=True, default=False, 
        verbose_name='Процесс смены статуса',
    )
    delivery_by_seller = models.BooleanField(
        editable=True, default=False,
        verbose_name='Доставка от продавца',
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
        verbose_name='Долг перед логистом по договору-заявке', 
    )
    logic_our_debt_UPD = models.FloatField(
        default=0,
        verbose_name='Долг перед логистом по УПД', 
    )
    logic_our_pay_amount = models.FloatField(
        default=0,
        verbose_name='Текущая сумма платежей перевозчику по сделке', 
    )
    payback_day_for_us = models.DateField(
        verbose_name='Дата оплаты для нас',
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
    deal_our_pay_amount = models.FloatField(
        default=0,
        verbose_name='Текущая сумма платежей продавцу по сделке', 
    )
    deal_buyer_pay_amount = models.FloatField(
        default=0,
        verbose_name='Текущая сумма платежей покупателя по сделке', 
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
    cB = models.PositiveIntegerField(
        verbose_name='Яйца СB, в десятках:', default=0,
    )
    c0 = models.PositiveIntegerField(
        verbose_name='Яйца С0, в десятках:', default=0,
    )
    c1 = models.PositiveIntegerField(
        verbose_name='Яйца С1, в десятках:', default=0,    
    )
    c2 = models.PositiveIntegerField(
        verbose_name='Яйца С2, в десятках:', default=0,
    )
    c3 = models.PositiveIntegerField(
        verbose_name='Яйца С3, в десятках:', default=0,
    )
    dirt = models.PositiveIntegerField(
        verbose_name='Грязь, в десятках:', default=0,
    )
    seller_cB_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c0_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c1_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0
    )
    seller_c2_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_c3_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    seller_dirt_cost = models.FloatField(
        verbose_name='Стоимость закупки за десяток', default=0,
    )
    buyer_cB_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c0_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c1_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0
    )
    buyer_c2_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_c3_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0
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
        self.margin = calculate_margin(self)

        if self.deal_our_pay_amount != self.__deal_our_pay_amount:
            delta = self.deal_our_pay_amount - self.__deal_our_pay_amount 
            change_client_balance_deal(self.seller, delta, self.cash) 

        if self.deal_buyer_pay_amount != self.__deal_buyer_pay_amount:
            delta = self.deal_buyer_pay_amount - self.__deal_buyer_pay_amount 
            change_client_balance_deal(self.buyer, delta, self.cash) 

        if self.logic_our_pay_amount != self.__logic_our_pay_amount:
            delta = self.logic_our_pay_amount - self.__logic_our_pay_amount
            if self.delivery_form_payment == 3:
                change_client_balance_deal(self.current_logic, delta, True)
            else:
                change_client_balance_deal(self.current_logic, delta, False)

        super(BaseDealEggsModel, self).save(*args, **kwargs)

    def __str__(self):
        return f'Базовая сделка №{self.pk}, статус №{self.status}'
