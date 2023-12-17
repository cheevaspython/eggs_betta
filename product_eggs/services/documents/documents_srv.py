import logging
from datetime import datetime
from django.db import transaction
from collections import OrderedDict

from product_eggs.models.balance import BalanceBaseClientEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.services.data_class.data_class_documents import PayOrderDataForSave
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.get_anything.get_patch_data_before_save import get_half_link_for_save
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from product_eggs.services.tails.tails import tail_return_to_balance_and_del_old
from users.models import CustomUser

logger = logging.getLogger(__name__)


def deal_docs_dict_json_update(
        serializer_data: OrderedDict,
        user: CustomUser,
        instance: DocumentsDealEggsModel) -> None:
    """
    may be delete? TODO
    """
    deal_docs_filefields = ('payment_order_incoming', 'payment_order_outcoming',
        'specification_seller', 'account_to_seller', 'specification_buyer',
        'account_to_buyer', 'application_contract_logic', 'account_to_logic',
        'UPD_incoming', 'account_invoicing_from_seller', 'product_invoice_from_seller',
        'UPD_outgoing', 'account_invoicing_from_buyer', 'product_invoice_from_buyer',
        'veterinary_certificate_buyer', 'veterinary_certificate_seller',
        'international_deal_CMR', 'international_deal_TTN_seller', 'UPD_logic',
        'account_invoicing_logic', 'product_invoice_logic', 'payment_order_outcoming_logic',
        'UPD_outgoing_signed', 'international_deal_TTN_buyer'
    )
    for item in serializer_data:
        if item in deal_docs_filefields:
            deal_dict_json = {
                "user": user.pk,
                "document_type": item,
                "document_link": (get_half_link_for_save(item) +
                    str(serializer_data[item])),
            }
            instance.deal_docs_links_json.update({str(datetime.today()) : deal_dict_json})
            instance.save()


@try_decorator_param(('KeyError',))
def check_logic_UPD(serializer_data: OrderedDict,
        request_data: OrderedDict,
        instance: DocumentsDealEggsModel) -> None:
    """
    If UPD_logic -> send message to role 7
    """
    if serializer_data['UPD_logic']:
        current_deal = BaseDealEggsModel.objects.get(documents=instance.pk)
        match current_deal.delivery_type_of_payment:
            case 1:
                message = MessageLibrarrySend(
                    'message_50_50_payment',
                    current_deal,
                )
                message.send_message()
            case 2:
                message = MessageLibrarrySend(
                    'message_100_payment',
                    current_deal,
                )
                message.send_message()
            case 3:
                if amount_advance := parse_request_data_for_amount_advance(request_data):
                    current_deal = BaseDealEggsModel.objects.get(documents=instance.pk)
                    message = MessageLibrarrySend(
                        'message_advance_payment',
                    current_deal,
                    amount_advance,
                    )
                    message.send_message()
            case _:
                logging.warning('case_ in services/docs_srv')


def parse_request_data_for_amount_advance(request_data: OrderedDict) -> str | None:
    try:
        return request_data['amount_advance']
    except KeyError:
        return None


@transaction.atomic
def subtract_deal_pays_then_del_datanum(
    cur_data_num: PayOrderDataForSave,
    cur_balance: BalanceBaseClientEggs,
    json_key: str,
    ) -> None:
    current_deal = BaseDealEggsModel.objects.get(pk=cur_data_num.deal)
    match cur_data_num.doc_type:
        case 'UPD_incoming' | 'UPD_outgoing' | 'UPD_logic':
            if cur_data_num.doc_type == 'UPD_incoming' and cur_data_num.client_type == 'seller':
                current_deal.deal_our_pay_amount += cur_data_num.pay_quantity
                current_deal.deal_our_debt_UPD = 0
                current_deal.documents.UPD_incoming = None
            elif cur_data_num.doc_type == 'UPD_outgoing' and cur_data_num.client_type == 'buyer':
                current_deal.deal_buyer_pay_amount += cur_data_num.pay_quantity
                current_deal.deal_buyer_debt_UPD = 0
                current_deal.documents.UPD_outgoing = None
            elif cur_data_num.doc_type == 'UPD_logic' and cur_data_num.client_type == 'logic':
                current_deal.logic_our_pay_amount += cur_data_num.pay_quantity
                current_deal.logic_our_debt_UPD = 0
                current_deal.documents.UPD_logic = None
        case 'payment_order_outcoming_logic' | 'payment_order_outcoming' | 'payment_order_incoming':
            if cur_data_num.doc_type == 'payment_order_outcoming' and cur_data_num.client_type == 'seller':
                current_deal.deal_our_pay_amount -= cur_data_num.pay_quantity
                current_deal.documents.payment_order_outcoming = None
            elif cur_data_num.doc_type == 'payment_order_incoming' and cur_data_num.client_type == 'buyer':
                current_deal.deal_buyer_pay_amount -= cur_data_num.pay_quantity
                current_deal.documents.payment_order_incoming = None
            elif cur_data_num.doc_type == 'payment_order_outcoming_logic' and cur_data_num.client_type == 'logic':
                current_deal.logic_our_pay_amount -= cur_data_num.pay_quantity
                current_deal.documents.ayment_order_outcoming_logic = None
        case 'tail_payment' | 'multi_pay_order':
            if cur_data_num.doc_type == 'tail_payment' and cur_data_num.client_type == 'seller':
                current_deal.deal_our_pay_amount -= cur_data_num.pay_quantity
                tail_return_to_balance_and_del_old(cur_data_num, cur_balance, cash=current_deal.cash)
            elif cur_data_num.doc_type == 'tail_payment' and cur_data_num.client_type == 'buyer':
                current_deal.deal_buyer_pay_amount -= cur_data_num.pay_quantity
                tail_return_to_balance_and_del_old(cur_data_num, cur_balance, cash=current_deal.cash)
            elif cur_data_num.doc_type == 'tail_payment' and cur_data_num.client_type == 'logic':
                current_deal.logic_our_pay_amount -= cur_data_num.pay_quantity
                tail_return_to_balance_and_del_old(cur_data_num, cur_balance, cash=current_deal.cash)

            elif cur_data_num.doc_type == 'multi_pay_order' and cur_data_num.client_type == 'seller':
                current_deal.deal_our_pay_amount -= cur_data_num.pay_quantity
                ...#TODO
            elif cur_data_num.doc_type == 'multi_pay_order' and cur_data_num.client_type == 'buyer':
                current_deal.deal_buyer_pay_amount -= cur_data_num.pay_quantity
            elif cur_data_num.doc_type == 'multi_pay_order' and cur_data_num.client_type == 'logic':
                current_deal.logic_our_pay_amount -= cur_data_num.pay_quantity

    if current_deal.cash:
        del current_deal.documents.data_number_json_cash[json_key]
    else:
        del current_deal.documents.data_number_json[json_key]

    current_deal.save()
    current_deal.documents.save()








