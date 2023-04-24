from datetime import datetime
from collections import OrderedDict

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.documents.docs_get_link import get_half_link_for_save
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from users.models import CustomUser


def deal_docs_dict_json_update(
        serializer_data: OrderedDict,
        user: CustomUser,
        instance: DocumentsDealEggsModel) -> None:
    """
    """
    deal_docs_filefields = ('payment_order_incoming', 'payment_order_outcoming',
        'specification_seller', 'account_to_seller', 'specification_buyer',
        'account_to_buyer', 'application_contract_logic', 'account_to_logic',
        'UPD_incoming', 'account_invoicing_from_seller', 'product_invoice_from_seller',
        'UPD_outgoing', 'account_invoicing_from_buyer', 'product_invoice_from_buyer',
        'veterinary_certificate_buyer', 'veterinary_certificate_seller',
        'international_deal_CMR', 'international_deal_TTN', 'UPD_logic', 
        'account_invoicing_logic', 'product_invoice_logic', 'payment_order_outcoming_logic',
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
                pass
            case _:
                print('wtf !!!')

    if amount_advance := parse_request_data_for_amount_advance(request_data):
        current_deal = BaseDealEggsModel.objects.get(documents=instance.pk)
        message = MessageLibrarrySend(
            'message_advance_payment',
            current_deal,
            amount_advance,
        )
        message.send_message()

    
def parse_request_data_for_amount_advance(request_data: OrderedDict) -> str:
    try:
        return request_data['amount_advance']
    except KeyError:
        return '0'
