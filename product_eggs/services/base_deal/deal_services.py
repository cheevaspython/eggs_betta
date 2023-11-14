from collections import OrderedDict

from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q

from rest_framework import serializers

from product_eggs.models.base_client import LogicCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.services.create_model import CreatorNewModel
from product_eggs.serializers.additional_expense_serializers import AdditionalExpenseSerializer
from users.models import CustomUser


def check_status_then_change():
    """
    Check fields base_model, then change next status.
    Raise if ...
    """

def check_relation_return_new_deal_docs(
        instance: BaseDealEggsModel) -> DocumentsDealEggsModel:
    """
    Создает внешний ключ на модель документов по сделке.
    if sucess set deal status -> 1.
    """
    if instance.documents is None:
        deal_doc_models = CreatorNewModel(
            ('DocumentsDealEggsModel', 'OriginsDealEggs'))
        deal_doc_models.create()
        deal_doc_models.new_models[0].origins = deal_doc_models.new_models[1]
        return  deal_doc_models.new_models[0]
    else:
        raise serializers.ValidationError(
            f'base model: {instance}, docs field has relation!')


def delivery_by_seller_check_and_return_logic(instance: BaseDealEggsModel) -> LogicCardEggs:
    try:
        return LogicCardEggs.objects.get(inn=instance.seller.inn)
    except (ObjectDoesNotExist, KeyError):
        raise serializers.ValidationError(
            'Доставка от продавца - ошибка: Указанный в просчете продавец не числится в базе перевозчиков. \
            Создайте перевозчика для данного продавца.')


def check_pre_status_for_create(
        instance: BaseDealEggsModel, status: int) -> None:
    """
    Check previous status base model.
    """
    if instance.status != status:
        serializers.ValidationError(
            f'in model: {instance}, status: {status}, cant update model.')


def get_additional_exp_detail(instance: BaseDealEggsModel) -> OrderedDict:
    """
    Возвращает детали дополнительного расхода по сделке.
    """
    model = AdditionalExpenseEggs.objects.get(id=instance.additional_expense)
    return_data = AdditionalExpenseSerializer(model)
    return return_data.data


def status_check(instance: BaseDealEggsModel, status: list[int]) -> None:
    """
    Check status calc, conf_calc, deal, complete_deal.
    """
    if instance.status not in status:
        raise serializers.ValidationError(f'Check status base_model, entry data, instance: {instance}, status: {instance.status}')


def base_deal_logs_saver(
        instance: BaseDealEggsModel, serializer_data: OrderedDict) -> None:
    """
    Save data in create or change moment, model BaseDealEggsModel.
    """
    match instance.status:
        case 1:
            instance.log_status_calc_query.update({**serializer_data})
            instance.save()
        case 2:
            instance.log_status_conf_calc_query.update({**serializer_data})
            instance.save()
        case 3:
            instance.log_status_deal_query.update({**serializer_data})
            instance.save()
        case _:
            pass


def base_deal_edit_saver(
        instance: BaseDealEggsModel,
        serializer_data: OrderedDict,
        user: CustomUser) -> None:
    """
    Save data in create or change moment, model BaseDealEggsModel.
    """
    date = str(datetime.today())
    instance.log_status_edit_query.update({date: {'edited_by': user.username, 'data': {**serializer_data}}})
    instance.save()


def get_sum_seller(instance: BaseDealEggsModel) -> float:
    """
    calc sum product for current deal model
    """
    sum_seller = (
        instance.cB_white*instance.seller_cB_white_cost +
        instance.cB_cream*instance.seller_cB_cream_cost +
        instance.cB_brown*instance.seller_cB_brown_cost +
        instance.c0_white*instance.seller_c0_white_cost +
        instance.c0_cream*instance.seller_c0_cream_cost +
        instance.c0_brown*instance.seller_c0_brown_cost +
        instance.c1_white*instance.seller_c1_white_cost +
        instance.c1_cream*instance.seller_c1_cream_cost +
        instance.c1_brown*instance.seller_c1_brown_cost +
        instance.c2_white*instance.seller_c2_white_cost +
        instance.c2_cream*instance.seller_c2_cream_cost +
        instance.c2_brown*instance.seller_c2_brown_cost +
        instance.c3_white*instance.seller_c3_white_cost +
        instance.c3_cream*instance.seller_c3_cream_cost +
        instance.c3_brown*instance.seller_c3_brown_cost +
        instance.dirt*instance.seller_dirt_cost
    )
    return sum_seller


def get_sum_buyer(instance: BaseDealEggsModel) -> float:

    sum_buyer = (
        instance.cB_white*instance.buyer_cB_white_cost +
        instance.cB_cream*instance.buyer_cB_cream_cost +
        instance.cB_brown*instance.buyer_cB_brown_cost +
        instance.c0_white*instance.buyer_c0_white_cost +
        instance.c0_cream*instance.buyer_c0_cream_cost +
        instance.c0_brown*instance.buyer_c0_brown_cost +
        instance.c1_white*instance.buyer_c1_white_cost +
        instance.c1_cream*instance.buyer_c1_cream_cost +
        instance.c1_brown*instance.buyer_c1_brown_cost +
        instance.c2_white*instance.buyer_c2_white_cost +
        instance.c2_cream*instance.buyer_c2_cream_cost +
        instance.c2_brown*instance.buyer_c2_brown_cost +
        instance.c3_white*instance.buyer_c3_white_cost +
        instance.c3_cream*instance.buyer_c3_cream_cost +
        instance.c3_brown*instance.buyer_c3_brown_cost +
        instance.dirt*instance.buyer_dirt_cost
    )
    return sum_buyer


def search_payments(client_type: str, payment_date: datetime | str):
    """
    search not close finance deals, filter for client
    """
    if isinstance(payment_date, str):
        date_save = datetime.strptime(payment_date,"%Y-%m-%d")
    else:
        date_save = payment_date

    match client_type:
        case 'seller':
            seller_deals = BaseDealEggsModel.objects.exclude(
                documents=None
            ).exclude(
                Q(documents__UPD_incoming='') # | Q(documents__payment_order_outcoming='')
            ).exclude(
                deal_our_pay_amount=0
            ).filter(
                payback_day_for_us__lte=date_save
            ).select_related(
                'documents', 'seller', 'buyer', 'current_logic'
            ).annotate(
                seller_name_orm = F('seller__requisites__name'),
                buyer_name_orm = F('buyer__requisites__name'),
                logic_name_orm = F('current_logic__requisites__name'),
            ).order_by("payback_day_for_us")
            return seller_deals
        case 'buyer':
            buyer_deals = BaseDealEggsModel.objects.exclude(
                documents=None
            ).exclude(
                Q(documents__UPD_outgoing='') # | Q(documents__payment_order_incoming='')
            ).exclude(
                deal_buyer_pay_amount=0
            ).filter(
                payback_day_for_buyer__lte=date_save
            ).select_related(
                'documents', 'seller', 'buyer', 'current_logic'
            ).annotate(
                seller_name_orm = F('seller__requisites__name'),
                buyer_name_orm = F('buyer__requisites__name'),
                logic_name_orm = F('current_logic__requisites__name'),
            ).order_by("payback_day_for_buyer")
            return buyer_deals
        case 'logic':
            logic_deals = BaseDealEggsModel.objects.exclude(
                documents=None
            ).exclude(
                Q(documents__UPD_logic='') #| Q(documents__payment_order_outcoming_logic='')
            ).exclude(
                logic_our_pay_amount=0
            ).filter(
                payback_day_for_us_logic__lte=date_save
            ).select_related(
                'documents', 'seller', 'buyer', 'current_logic'
            ).annotate(
                seller_name_orm = F('seller__requisites__name'),
                buyer_name_orm = F('buyer__requisites__name'),
                logic_name_orm = F('current_logic__requisites__name'),
            ).order_by("payback_day_for_us_logic")
            return logic_deals
        case _:
            return None


def finance_discipline_search(client_type: str, client_inn: str):
    """
    """
    match client_type:
        case 'seller':
            seller_deals = BaseDealEggsModel.objects.exclude(
                documents=None
            ).filter(
                seller=client_inn
            ).exclude(
                Q(documents__UPD_incoming='')
            ).filter(
                deal_our_pay_amount=0
            ).select_related(
                'documents', 'seller',
            ).annotate(
                seller_name_orm = F('seller__requisites__name'),
            )
            return seller_deals

        case 'buyer':
            buyer_deals = BaseDealEggsModel.objects.exclude(
                documents=None
            ).filter(
                buyer=client_inn
            ).exclude(
                Q(documents__UPD_outgoing='')
            ).filter(
                deal_buyer_pay_amount=0
            ).select_related(
                'documents', 'buyer'
            ).annotate(
                buyer_name_orm = F('buyer__requisites__name'),
            )
            return buyer_deals

        case 'logic':
            logic_deals = BaseDealEggsModel.objects.exclude(
                documents=None
            ).filter(
                current_logic=client_inn
            ).exclude(
                Q(documents__UPD_logic='')
            ).filter(
                logic_our_pay_amount=0
            ).select_related(
                'documents', 'current_logic'
            ).annotate(
                logic_name_orm = F('current_logic__requisites__name'),
            )
            return logic_deals
        case _:
            return None












