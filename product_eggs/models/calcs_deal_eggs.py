from django.db import models
from django.core import validators
        
from product_eggs.models.apps_eggs import ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
from product_eggs.models.base_eggs import LogicCardEggs
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.tasks import change_client_balance_deal
from users.models import CustomUser
    

class CalculateEggs(models.Model):
    PAY_TYPE = ((20, 'С  НДС'), (0, 'Без НДС'))

    class Meta:
        db_table = 'CalculateEggs'
        verbose_name = 'Просчет'
        verbose_name_plural = 'Просчеты'
        ordering = ['pk']

    application_from_buyer = models.ForeignKey(
        ApplicationFromBuyerBaseEggs, on_delete=models.PROTECT,
        verbose_name='Заявка от покупателя',
    )
    application_from_seller = models.ForeignKey(
        ApplicationFromSellerBaseEggs, on_delete=models.PROTECT,
        verbose_name='Заявка от продавца',
    )
    delivery_cost = models.FloatField( 
        verbose_name='Средняя стоимость доставки', default=0, 
    )
    delivery_type_of_payment = models.PositiveSmallIntegerField(
        verbose_name='Тип оплаты', choices=PAY_TYPE, default=20,
    )
    delivery_by_seller = models.BooleanField(
        editable=True, default=False, verbose_name='Доставка от продавца',
    )
    owner = models.ForeignKey(
        CustomUser, related_name='calculate', verbose_name='Автор просчета',
        on_delete=models.SET_NULL, null=True,
    )
    is_active = models.BooleanField(
        editable=True, default=True, verbose_name='is_active',
    )
    comment = models.CharField(
        max_length=255, verbose_name='Комментарий', null=True, blank=True
    )
    delivery_date_from_seller = models.DateField(
        verbose_name='Дата погрузки', null=True, 
    )
    delivery_date_to_buyer = models.DateField(
        verbose_name='Дата поставки', null=True,
    )
    cash = models.BooleanField(
        editable=True, default=False, verbose_name='Продажа за нал'
    )
    cB = models.PositiveIntegerField(
        verbose_name='Яйца СВ, в десятках:', default=0,     
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
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_dirt_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    loading_address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Адрес погрузки',
    )
    unloading_address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Адрес разгрузки',
    )
    pre_payment_application = models.BooleanField(
        editable=True, default=True, verbose_name='Предоплата',
    )
    import_application = models.BooleanField(
        editable=True, default=False, verbose_name='Импорт',
    )
    seller_name = models.CharField(
        max_length=255, verbose_name='Покупатель', null=True,    
    )
    buyer_name = models.CharField(
        max_length=255, verbose_name='Продавец', null=True,    
    )
    buyer_inn = models.CharField(
        max_length=12, verbose_name='ИНН покупатель', null=True,    
        validators=[validators.MaxLengthValidator(12), validators.MinLengthValidator(10)],
    )
    seller_inn = models.CharField(
        max_length=12, verbose_name='ИНН продавец', null=True,
        validators=[validators.MaxLengthValidator(12), validators.MinLengthValidator(10)],
    )
    note = models.TextField(
        verbose_name='Замечание', null=True, blank=True,    
    )
    postponement_pay_for_us = models.PositiveIntegerField(
        default=0, verbose_name='Отсрочка оплаты для нас',
    )
    postponement_pay_for_buyer = models.PositiveIntegerField(
        default=0, verbose_name='Отсрочка оплаты для покупателя',
    )

    def __str__(self):
        return f'Просчет №{self.pk}'


class ConfirmedCalculateEggs(models.Model):
    PAY_TYPE = ((20, 'С  НДС'), (0, 'Без НДС'))

    class Meta:
        db_table = 'ConfirmedCalculateEggs'
        verbose_name = 'Просчет подтвержденный'
        verbose_name_plural = 'Просчеты подтвержденные'
        ordering = ['pk']

    current_calculate = models.ForeignKey(
        CalculateEggs, on_delete=models.PROTECT, verbose_name='Просчет', null=True, blank=True,
    )
    current_logic = models.ForeignKey(
        LogicCardEggs, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Логист',
    )
    delivery_cost = models.FloatField( 
        verbose_name='Стоимость доставки', default=0, 
    )
    delivery_type_of_payment = models.PositiveSmallIntegerField(
        verbose_name='Тип оплаты', choices=PAY_TYPE, default=20
    )
    delivery_date_from_seller = models.DateField(
        verbose_name='Дата погрузки', null=True, 
    )
    delivery_date_to_buyer = models.DateField(
        verbose_name='Дата поставки', null=True,
    )
    calc_ready = models.BooleanField(
        editable=True, default=False, verbose_name='Просчет готов',
    )
    logic_confirmed = models.BooleanField(
        editable=True, default=False, verbose_name='Логист добавлен',
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Создана',
    )
    edited = models.DateTimeField(
        auto_now=True, verbose_name='Изменена',
    )
    owner = models.ForeignKey(
        CustomUser, related_name='confirmed_calculate',
        verbose_name='Автор подтвержденного просчета',
        on_delete=models.SET_NULL, null=True,
    )
    is_active = models.BooleanField(
        editable=True, default=True, verbose_name='is_active',
    )
    comment = models.CharField(
        max_length=255, verbose_name='Комментарий', null=True, blank=True,
    )
    note = models.TextField(
        verbose_name='Замечание', null=True, blank=True,    
    )
    additional_expense = models.OneToOneField(
        AdditionalExpenseEggs, on_delete=models.PROTECT, 
        verbose_name='Доп Расход', null=True,
    )
    def __str__(self):
        return f'Просчет подтвержденный №{self.pk}'

class DealEggs(models.Model):
    PAY_TYPE = ((20, 'С  НДС'), (0, 'Без НДС'))

    
    class Meta:
        db_table = 'DealEggs'
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
        ordering = ['pk']

    confirmed_calculate = models.OneToOneField(
        ConfirmedCalculateEggs, on_delete=models.PROTECT,
        verbose_name='Просчет подтвержденный', null=True,
    )
    STATUS = (
    (1, 'на подтверждении у фин. директора'),
    (2, 'на ожидании основания платежа от продавца'),
    (3, 'на подтверждении у фин. директора (по оплате счета от продавца'),
    (4, 'на ожидании оплаты и загрузки бухгалтером счета от продавца'),
    (5, 'на погрузке и ожидании УПД от продавца'),
    (6, 'товар в пути, ожидаем запрос на исходящую УПД'),
    (7, 'на ожидании загрузки исходящей УПД бухгалтером'),
    (8, 'на разгрузке, ожидаем подписанную УПД'),
    (9, 'на ожидании закрывающих документов'),
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS, default=1, verbose_name='Статус',
    )
    processing_to_confirm = models.BooleanField(
        editable=True, default=True, verbose_name='processing_to_confirm',
    )
    actual_loading_date = models.DateField(
        verbose_name='Фактическая дата погрузки', blank=True, null=True, 
    )
    actual_unloading_date = models.DateField(
        verbose_name='Фактическая дата разгрузки', blank=True, null=True,
    )
    is_active = models.BooleanField(
        editable=True, default=True, verbose_name='is_active',
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Создана',
    )
    edited = models.DateTimeField(
        auto_now=True, verbose_name='Изменена',
    )
    owner = models.ForeignKey(CustomUser, related_name='owner',
        verbose_name='автор', on_delete=models.SET_NULL, null=True,
    )
    documents = models.OneToOneField(
        DocumentsDealEggsModel,on_delete=models.PROTECT, 
        verbose_name='Документы по сделке', null=True,
    )
    comment = models.CharField(
        max_length=1000, verbose_name='Комментарий',
        null=True, blank=True,
    )
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
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    buyer_dirt_cost = models.FloatField(
        verbose_name='Стоимость продажи за десяток', default=0,
    )
    seller_manager = models.ForeignKey(
        CustomUser, related_name='seller_manager_deal',
        verbose_name='Менеджер сделки от продавца',
        on_delete=models.SET_NULL, null=True
    )
    buyer_manager = models.ForeignKey(
        CustomUser, related_name='buyer_manager_deal',
        verbose_name='Менеджер сделки от покупателя',
        on_delete=models.SET_NULL, null=True
    )
    delivery_cost = models.FloatField(
        verbose_name='Стоимость доставки', default=0, 
    )
    delivery_type_of_payment = models.PositiveSmallIntegerField(
        verbose_name='Тип оплаты', choices=PAY_TYPE, default=20,
    )
    delivery_date_from_seller_from_calc = models.DateField(
        verbose_name='Дата погрузки', null=True, 
    )
    delivery_date_to_buyer_from_calc = models.DateField(
        verbose_name='Дата поставки', null=True, 
    )
    delivery_by_seller = models.BooleanField(
        editable=True, default=False, verbose_name='Доставка от продавца',
    )
    loading_address = models.CharField(
        max_length=255, null=True, verbose_name='Адрес погрузки',
    )
    unloading_address = models.CharField(
        max_length=255, null=True, verbose_name='Адрес разгрузки',
    )
    buyer_inn = models.CharField(
        max_length=12, verbose_name='ИНН покупатель', null=True,    
        validators=[validators.MaxLengthValidator(12),
        validators.MinLengthValidator(10)],
    )
    seller_inn = models.CharField(
        max_length=12, verbose_name='ИНН продавец', null=True,    
        validators=[validators.MaxLengthValidator(12),
        validators.MinLengthValidator(10)],
    )
    seller_name = models.CharField(
        max_length=255, verbose_name='Покупатель', null=True,    
    )
    buyer_name = models.CharField(
        max_length=255, verbose_name='Продавец', null=True,    
    )
    cash = models.BooleanField(
	    editable=True, default=False, verbose_name='Продажа за нал',
    )
    additional_expense = models.CharField(
        max_length=255, verbose_name='Расход', null=True,    
    )
    current_logic = models.ForeignKey(
        LogicCardEggs, on_delete=models.PROTECT, null=True, verbose_name='Логист',
    )
    payback_day_for_us = models.DateField(
        verbose_name='Дата оплаты для нас', null=True, blank=True, 
    )
    payback_day_for_buyer = models.DateField(
        verbose_name='Дата оплаты для покупателя', null=True, blank=True, 
    )
    postponement_pay_for_us = models.PositiveIntegerField(
        default=0, verbose_name='Отсрочка оплаты для нас'
    )
    postponement_pay_for_buyer = models.PositiveIntegerField(
        default=0, verbose_name='Отсрочка оплаты для покупателя'
    )
    pre_payment_application = models.BooleanField(
        editable=True, default=True, verbose_name='Предоплата'
    )
    import_application = models.BooleanField(
        editable=True, default=False, verbose_name='Импорт'
    )
    current_deal_our_debt = models.FloatField(
        null=True, blank=True, default=0,
        verbose_name='Текущий долг перед продавцом по сделке', 
    )
    current_deal_buyer_debt = models.FloatField(
        null=True, blank=True, default=0,
        verbose_name='Текущий долг покупателя по сделке', 
    )
    deal_our_debt_UPD = models.FloatField(
        null=True, blank=True, default=0,
        verbose_name='Долг перед продавцом по сделке по УПД', 
    )
    deal_buyer_debt_UPD = models.FloatField(
        null=True, blank=True, default=0,
        verbose_name='Долг перед нами по сделке по УПД', 
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__current_deal_our_debt = self.current_deal_our_debt
        self.__current_deal_buyer_debt = self.current_deal_buyer_debt

    def save(self, *args, **kvargs):
        self.current_deal_buyer_debt = round(self.current_deal_buyer_debt, 2)
        self.current_deal_our_debt = round(self.current_deal_our_debt, 2)

        if self.current_deal_our_debt != self.__current_deal_our_debt:
            delta = self.__current_deal_our_debt - self.current_deal_our_debt 
            change_client_balance_deal(self.seller_inn, delta, self.cash) 

        if self.current_deal_buyer_debt != self.__current_deal_buyer_debt:
            delta = self.__current_deal_buyer_debt - self.current_deal_buyer_debt 
            change_client_balance_deal(self.buyer_inn, delta, self.cash) 

        super(DealEggs, self).save(*args, **kvargs)

    def __str__(self):
        return f'Сделка №{self.pk}'


