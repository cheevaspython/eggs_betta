from collections import OrderedDict

from rest_framework import serializers
from product_eggs.models.additional_expense import AdditionalExpenseEggs

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.create_model import  CreatorNewModel
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.messages.messages_library import MessageLibrarrySend
                 

def check_fields_values_to_calc_ready(instance: BaseDealEggsModel) -> bool | None:
    if instance.status == 2:
        conf_calc_fields = (instance.current_logic,
            instance.delivery_date_from_seller,
            instance.delivery_date_to_buyer,
            instance.delivery_cost,
            instance.logic_confirmed,
        )
        for item in conf_calc_fields:
            if item is None or False:
                instance.calc_ready = False
                instance.save()
                raise serializers.ValidationError(
                    f'Для продолжения заполните {item}')
        return True


def check_calc_ready_for_true(base_model: BaseDealEggsModel) -> None: 
    if base_model.calc_ready:
        raise serializers.ValidationError('Просчет уже на подтверждении!')


def check_field_expence_create_new_model(
        instance: BaseDealEggsModel) -> None | AdditionalExpenseEggs:
    """
    Check field BaseDealEggsModel.additional_expense, then 
    change status for 2 (create conf_calc), 
    if not none -> raise error,
    else return new_model for relate.
    """
    if instance.additional_expense:
        raise serializers.ValidationError('additional_expense not None') 
    else:
        new_model = CreatorNewModel(('AdditionalExpenseEggs',))
        new_model.create()
        return new_model.new_models[0]


@try_decorator_param(('AttributeError','KeyError',))
def check_validated_data_for_logic_conf(
        validated_data: OrderedDict, instance: BaseDealEggsModel) -> None:
    """
    Check serializer validated_data path conf_calc status, 
    for bool logic_confirmed. 
    """
    if validated_data['logic_confirmed']:
        message = MessageLibrarrySend('logic_confirmed', instance)
        message.send_message()


