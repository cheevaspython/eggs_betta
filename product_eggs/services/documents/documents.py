from dataclasses import asdict
from datetime import datetime
from collections import OrderedDict

from product_eggs.models.documents import DocumentsBuyerEggsModel, \
    DocumentsDealEggsModel
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.documents.docs_get_link import get_half_link_for_save
from product_eggs.services.data_class import PayOrderDataForSaveMulti
from product_eggs.services.documents.documents_get import update_and_save_data_number_json
from users.models import CustomUser


def deal_docs_dict_json_update(
        serializer_data: OrderedDict,
        user: CustomUser,
        instance: DocumentsDealEggsModel) -> None:
    """
    Сверяет документ со списком, сохраняет в словарь при корректности данных.
    """
    deal_docs_filefields = ('payment_order_incoming', 'payment_order_outcoming',
        'specification_seller', 'account_to_seller', 'specification_buyer',
        'account_to_buyer', 'application_contract_logic', 'account_to_logic',
        'UPD_incoming', 'account_invoicing_from_seller', 'product_invoice_from_seller',
        'UPD_outgoing', 'account_invoicing_from_buyer', 'product_invoice_from_buyer',
        'veterinary_certificate_buyer', 'veterinary_certificate_seller',
        'international_deal_CMR', 'international_deal_TTN', 'UPD_logic', 
        'account_invoicing_logic', 'product_invoice_logic', )

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


@try_decorator_param(('TypeError',))
def cash_documents_check_save(
        tmp_json_data: dict,
        user: CustomUser,
        instance: DocumentsBuyerEggsModel) -> None:
    """
    Сохраняет данные по вводу по форме 2.
    """
    tmp_json_data['user'] = user.pk
    check_json_data = PayOrderDataForSaveMulti(**tmp_json_data) 
    update_and_save_data_number_json(asdict(check_json_data), instance)

