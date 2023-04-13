from dataclasses import asdict
from datetime import datetime
from typing import Union
from collections import OrderedDict

from rest_framework import serializers

from product_eggs.models.documents import DocumentsBuyerEggsModel, \
    DocumentsContractEggsModel, DocumentsDealEggsModel
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs
from product_eggs.models.calcs_deal_eggs import DealEggs
from product_eggs.services.base_client_services import get_client_for_inn
from product_eggs.services.docs_get_link import get_half_link_for_save
from product_eggs.services.messages_library import send_message_to_finance_director 
from product_eggs.services.deal_services import DealPayOrderUPDservice, \
    try_to_get_deal_model_for_doc_deal_id
from product_eggs.services.data_class import PayOrderDataForSave, PayOrderDataForSaveMulti
from product_eggs.services.statistic import ContragentBalanceForm
from product_eggs.services.documents_get import update_and_save_data_number_json
from product_eggs.services.tails import tails_treatment
from users.models import CustomUser


def try_to_write_date_nums_jsonfield(pay_data: OrderedDict, user: CustomUser,
        instance: DocumentsDealEggsModel) -> None:
    """
    Обрабатывает вводимые данные по значимым платежным документам.
    Создает dataclass и взаимодействует с DealPayOrderUPDservice 
    Записывает данные в случае корректности, либо raise error.
    """
    current_deal = try_to_get_deal_model_for_doc_deal_id(instance.pk)
    if isinstance(current_deal, DealEggs): 
        pay_order_client  = get_client_for_inn(pay_data['inn']) 
        if isinstance(pay_order_client , Union[SellerCardEggs, BuyerCardEggs]):
            pay_data['user'] = user.pk
            pay_data['deal'] = current_deal.pk
            pay_data['documents_id'] = instance.pk
            pay_order_data = PayOrderDataForSave(**pay_data) 

            update_and_save_data_number_json(pay_data, instance)
            update_and_save_data_number_json(
                pay_data, pay_order_client.documents_contract)

            deal_service_object = DealPayOrderUPDservice(
                pay_order_data,
                current_deal,
                pay_order_client,
                ContragentBalanceForm(
                    current_deal=current_deal,
                    pay_client=pay_order_client,
                    money_amount=float(pay_order_data.pay_quantity),
                )
            )
            deal_service_object.try_to_create_payback_date_if_UPD_update()
            deal_service_object.add_or_replay_deal_debt() 
            deal_service_object.deal.save()
        else:
            serializers.ValidationError('client id is not valid')
    else:
        serializers.ValidationError('deal id invalid. check entry data')


def parse_multy_payment_json(
        tmp_multy_pay_order_data,
        user: CustomUser,
        current_document_contract: DocumentsContractEggsModel | None) -> None:
    """
    Обрабатывает вводимые данные по значимым платежным документам.
    Создает dataclass и взаимодействует с DealPayOrderUPDservice 
    Записывает данные в случае корректности, либо raise error.
    при общем платежном поручении.
    """
    tmp_multy_pay_order_data['user'] = user.pk

    try:
        pay_order_data_multi = PayOrderDataForSaveMulti(**tmp_multy_pay_order_data) 
        pay_order_client  = get_client_for_inn(pay_order_data_multi.inn) 
    except TypeError as e:
        serializers.ValidationError(f'wrong tmp_mutli data error - {e}')
        pay_order_data_multi = None
        pay_order_client = None

    save_for_update_data = list()
    if pay_order_data_multi and pay_order_client:
        if pay_order_data_multi.other_pays:
            for deals_data in pay_order_data_multi.other_pays:
                current_deal = try_to_get_deal_model_for_doc_deal_id(deals_data.documents_id)
                if isinstance(current_deal, DealEggs) and isinstance(
                        pay_order_client, SellerCardEggs | BuyerCardEggs):

                    tmp_asdict = asdict(pay_order_data_multi)
                    tmp_asdict.pop('other_pays', None)
                    tmp_asdict.pop('total_amount', None)
                    tmp_asdict.pop('tail_form_one', None)
                    tmp_asdict.pop('tail_form_two', None)
                    tmp_asdict.update(asdict(deals_data))
                    pay_order_data = PayOrderDataForSave(**tmp_asdict) 

                    deal_service_object = DealPayOrderUPDservice(
                        pay_order_data,
                        current_deal,
                        pay_order_client,
                        ContragentBalanceForm(
                            current_deal=current_deal,
                            pay_client=pay_order_client,
                            money_amount=float(pay_order_data.pay_quantity),
                        )
                    )
                    deal_service_object.add_or_replay_deal_debt()  
                    save_for_update_data.append((deal_service_object, tmp_asdict, current_deal.documents,))

            for objects in save_for_update_data:
                objects[0].deal.save()
                update_and_save_data_number_json(objects[1], objects[2])

        tmp_asdict = asdict(pay_order_data_multi)
        
        send_message_to_finance_director(
            f"ПП от {pay_order_client}/{pay_order_data_multi.inn}" + 
            f"на сумму {pay_order_data_multi.total_amount}",
            pay_order_client,
        )
        if current_document_contract == None:
            current_document_contract = DocumentsContractEggsModel.objects.get(
                pk=pay_order_client.documents_contract.pk)

        if tmp_asdict['tail_form_one'] or tmp_asdict['tail_form_two']:
            tmp_asdict.pop('other_pays', None)
            tails_treatment(tmp_asdict, pay_order_client)

        current_document_contract.multy_pay_json.update( #TODO
            {str(datetime.today())[:-7]: tmp_asdict})

        update_and_save_data_number_json(
            tmp_asdict, current_document_contract)


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


def cash_documents_check_save(
        tmp_json_data: dict,
        user: CustomUser,
        instance: DocumentsBuyerEggsModel) -> None:
    """
    Сохраняет данные по вводу по форме 2.
    """
    tmp_json_data['user'] = user.pk

    try:
        check_json_data = PayOrderDataForSaveMulti(**tmp_json_data) 
        update_and_save_data_number_json(asdict(check_json_data), instance)
    except TypeError as e:
        print(e)





