from collections import OrderedDict

from rest_framework import serializers

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.services.create_model import CreatorNewModel
from product_eggs.serializers.additional_expense_serializers import AdditionalExpenseSerializer


def check_status_then_change():
    """
    Check fields base_model, then change next status.
    Raise if ...
    """

def create_relation_deal_status_and_deal_docs(
        instance: BaseDealEggsModel) -> None:
    """
    Создает внешний ключ на модель документов по сделке.
    if sucess set deal status -> 1.
    """
    if instance.documents is None:   
        deal_doc_models = CreatorNewModel(
            ('DocumentsDealEggsModel', 'OriginsDealEggs'))
        deal_doc_models.create()
        deal_doc_models.new_models[0].origins = deal_doc_models.new_models[1]
        instance.documents = deal_doc_models.new_models[0]
        instance.deal_status = 1 
        instance.save()
    else:
        raise serializers.ValidationError(
            f'base model: {instance}, docs field has relation!')


def check_pre_status_for_create(
        instance: BaseDealEggsModel, status: int) -> None:
    """
    Check previous status base model.
    """
    if instance.status != status:
        serializers.ValidationError(
            f'in model: {instance}, status: {status}, cant update model.')


def get_additional_exp_detail(instance: BaseDealEggsModel) -> OrderedDict: #TODO
    """
    Возвращает детали дополнительного расхода по сделке.
    """
    model = AdditionalExpenseEggs.objects.get(id=instance.additional_expense)
    return_data = AdditionalExpenseSerializer(model)
    return return_data.data


def status_check(instance: BaseDealEggsModel, status: int):
    """
    Check status calc, conf_calc, deal, complete_deal.
    """
    if instance.status != status:
        raise serializers.ValidationError('Check status base_model')

