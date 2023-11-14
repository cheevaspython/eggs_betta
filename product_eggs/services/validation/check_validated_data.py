import logging

from datetime import datetime

from typing import OrderedDict

from django.utils import timezone
from rest_framework import serializers

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsContractEggsModel, DocumentsDealEggsModel
from product_eggs.services.data_class.data_class_documents import (
    PrePayOrderDataForSave, PrePayOrderDataForSaveMulti
)
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.documents.documents_parse_tmp_json import (
    DealDocumentsPaymentParser, MultiDocumentsPaymentParser
)
from product_eggs.services.documents.documents_static import (
    DOC_CONTRACT_CASH, DOC_CONTRACT_CONTRACT, DOC_CONTRACT_MULTY_PAY
)
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from users.models import CustomUser

logger = logging.getLogger(__name__)


@try_decorator_param(('MultiValueDictKeyError', 'AttributeError', 'KeyError'))
def check_data_for_note(
        data: OrderedDict,
        instance: BaseDealEggsModel,
        note: str,
        cur_user: CustomUser) -> bool:
    """
    Проверяет наличие note в данных,
    отправляет note в виде сообщения если находит.
    """
    note_dict = {
        'note_calc': instance.note_calc,
        'note_conf_calc': instance.note_conf_calc,
    }
    if note in note_dict.keys():
        if data[note]:
            user_string = f'от {cur_user.username}: \n'
            new_message = MessageLibrarrySend(
                note,
                instance,
                user_string + data[note],
            )
            new_message.send_message()
            return True
    return False


def convert_front_data_to_prepaydataforsave(entry_data: OrderedDict) -> PrePayOrderDataForSave:
    try:
        pre_pay_data = PrePayOrderDataForSave(**entry_data['tmp_json'])
        return pre_pay_data
    except (KeyError, AttributeError) as e:
        raise serializers.ValidationError('wrong tmp_data for pay', e)


def convert_front_data_to_prepaydataforsavemulti(entry_data: OrderedDict) -> PrePayOrderDataForSaveMulti:
    try:
        pre_pay_data_multi = PrePayOrderDataForSaveMulti(**entry_data['tmp_json_multi_pay_order'])
        return pre_pay_data_multi
    except (KeyError, AttributeError) as e:
        raise serializers.ValidationError('wrong tmp_json_for_multi_pay_order for pay', e)


@try_decorator_param(('KeyError',))
def check_validated_data_for_tmp_json(
        serializer_data: OrderedDict,
        instance: DocumentsDealEggsModel,
        user: CustomUser) -> None:
    if serializer_data['tmp_json']:
        parser = DealDocumentsPaymentParser(
            convert_front_data_to_prepaydataforsave(serializer_data),
            user,
            instance,
        )
        parser.main_default()


@try_decorator_param(('KeyError',))
def check_val_data_contract_multy_pay(
        serializer_data: OrderedDict,
        instance: DocumentsContractEggsModel,
        user: CustomUser) -> bool:

    if check_data_for_value(serializer_data, 'multi_pay_order') and \
            check_data_for_value(serializer_data, 'tmp_json_multi_pay_order'):
        multi_data = convert_front_data_to_prepaydataforsavemulti(serializer_data)
        instance.multi_pay_order_links_dict_json.update(
            {str(datetime.today())[:-7]: (DOC_CONTRACT_MULTY_PAY +
                str(serializer_data['multi_pay_order']))}
        )
        parse_multi = MultiDocumentsPaymentParser(
            multi_data,
            user,
            instance,
        )
        parse_multi.main()
        return True

    elif check_data_for_value(serializer_data, 'tmp_json_multi_pay_order'):
        if serializer_data['tmp_json_multi_pay_order']['cash']:
            multi_data = convert_front_data_to_prepaydataforsavemulti(serializer_data)
            if check_data_for_value(serializer_data, 'multi_pay_order_cash'):
                instance.multi_pay_order_cash_links.update(
                    {str(datetime.today())[:-7]: (DOC_CONTRACT_CASH +
                        str(serializer_data['multi_pay_order_cash']))}
                )
            parse_multi = MultiDocumentsPaymentParser(
                multi_data,
                user,
                instance,
            )
            parse_multi.main()
            return True

        else:
            raise serializers.ValidationError(
                'wrong tmp_json_multi_pay_order data (tmp_json form1, but not multi_pay_order)')
    else:
        return False


@try_decorator_param(('KeyError',), return_value=False)
def check_data_for_value(serializer_data: OrderedDict, value: str) -> bool:
    return True if serializer_data[value] else False


@try_decorator_param(('KeyError',))
def check_val_data_contract_for_contract(
        serializer_data: OrderedDict,
        instance: DocumentsContractEggsModel) -> bool:
    if serializer_data['contract']:
        instance.contract_links_dict_json.update(
            {str(datetime.today())[:-7]: (DOC_CONTRACT_CONTRACT +
                str(serializer_data['contract']))}
        )
        instance.save()
        return True
    return False


def match_data_for_fresh_app(date: datetime):
    interval = timezone.now() - date
    if interval.days == 0:
        return '#09ff005e'
    elif interval.days <= 2:
        return '#fffb005e'
    else:
        return '#ff00005e'












