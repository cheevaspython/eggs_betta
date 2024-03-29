from collections import OrderedDict
from dataclasses import asdict
from datetime import datetime
from typing import Optional

from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.additional_exp_service import (
    parse_additional_tmp_json, parse_additional_tmp_multi_json
)
from product_eggs.services.create_model import  CreatorNewModel
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from product_eggs.services.validationerror import custom_error


def check_fields_values_to_calc_ready(instance: BaseDealEggsModel) -> bool | None:
    """
    Проверка полей при calc ready
    """
    if instance.status == 2 and instance.documents:
        conf_calc_fields = [instance.current_logic,
            instance.delivery_date_from_seller,
            instance.delivery_date_to_buyer,
            instance.delivery_cost,
            instance.logic_confirmed,
        ]
        if not instance.delivery_by_seller:
            conf_calc_fields += [instance.current_logic,
                instance.delivery_form_payment,
                instance.delivery_type_of_payment,
                instance.logic_our_debt_for_app_contract,
                instance.documents.application_contract_logic,
            ]
        for item in conf_calc_fields:
            if item is None or False:
                instance.calc_ready = False
                instance.save()
                raise custom_error(
                    f'Для продолжения заполните {item}'
                )
        return True


def request_data_chech_for_note(request_data: OrderedDict) -> bool:
    """
    Ищет в реквесте note_conf_calc
    """
    try:
        if request_data['note_conf_calc']:
            return True
        else:
            return False
    except (AttributeError, KeyError, TypeError):
        return False


def check_calc_ready_for_true(base_model: BaseDealEggsModel, request) -> None | OrderedDict:
    """
    Проверка bool calc_ready, в случае True -> Выдает предупреждение.
    """
    if base_model.calc_ready:
        if request_data_chech_for_note(request.data):
            request.data['calc_ready'] = False
            return request
        else:
            raise custom_error('Просчет уже на подтверждении!')


def check_field_expence_create_new_model(
        instance: BaseDealEggsModel) -> None | AdditionalExpenseEggs:
    """
    Check field BaseDealEggsModel.additional_expense, then
    change status for 2 (create conf_calc),
    if not none -> raise error,
    else return new_model for relate.
    """
    if instance.additional_expense:
        raise custom_error('additional_expense not None', 433)
    else:
        new_model = CreatorNewModel(('AdditionalExpenseEggs',))
        new_model.create()
        return new_model.new_models[0]


def expence_create_new_model(validated_data: Optional[OrderedDict] = None) -> AdditionalExpenseEggs:
    """
    return new_model for relate.
    """
    if validated_data:
        if data_for_save := parse_additional_tmp_json(validated_data):
            if data_for_save.cash:
                exp_data_for_create = {
                    'expense_detail_json': (
                        {str(datetime.today()) : asdict(data_for_save)}
                    ),
                    'expense_total_form_2': float(data_for_save.expense),
                    'tmp_json': {},
                }
            else:
                exp_data_for_create = {
                    'expense_detail_json': (
                        {str(datetime.today()) : asdict(data_for_save)}
                    ),
                    'expense_total_form_1': float(data_for_save.expense),
                    'tmp_json': {},
                }
            new_model = CreatorNewModel(('AdditionalExpenseEggs',), **exp_data_for_create)
            new_model.create()
        else:
            new_model = CreatorNewModel(('AdditionalExpenseEggs',), )
            new_model.create()
            if updated_exp := parse_additional_tmp_multi_json(new_model.new_models[0], validated_data):
                return updated_exp
    else:
        new_model = CreatorNewModel(('AdditionalExpenseEggs',), )
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











