import os
from datetime import datetime

from django.http import FileResponse
from django.conf import settings
from rest_framework import serializers

from product_eggs.models.documents import DocumentsDealEggsModel, DocumentsContractEggsModel


def parce_pk_data(pk: str) -> list[str]:
    """
    Парсинг в параметоризированной строке.
    """
    return pk.replace('-', ' ').split()


def get_auto_download_response(file_link: str | None) -> FileResponse | None:
    """
    Возвращает ссылку на скачивание документа.
    """
    if file_link:
        module_dir = os.path.join(settings.MEDIA_ROOT, file_link)   
        auto_download_response = FileResponse(open(module_dir, 'rb'), as_attachment=True)
        return auto_download_response
    else:
        raise serializers.ValidationError('v pk kakayato chush')


def start_the_desired_getter_link(model: str, pk: str, title: str) -> FileResponse | None:
    """
    Обрабатывает модель и значения для возвращения ссылки.
    """
    model_to_getter_link= {
        'contract': get_contract_fileresponse,
        'deal_docs': get_deal_docs_fileresponse,
    }
    return model_to_getter_link[model](pk, title)


def get_deal_docs_fileresponse(pk: str, title: str) -> FileResponse | None:
    """
    Получает линк модели DocumentsDealEggsModel. 
    """
    instance = DocumentsDealEggsModel.objects.get(id=pk)
    file_link = get_link_deal_docs(instance, title)
    auto_download_response = get_auto_download_response(file_link)
    return(auto_download_response)


def get_contract_fileresponse(pk: str, title: str) -> FileResponse | None:
    """
    Получает линк модели DocumentsContractEggsModel. 
    """
    instance = DocumentsContractEggsModel.objects.get(id=pk)
    file_link = get_link_contract(instance, title)
    auto_download_response = get_auto_download_response(file_link)
    return(auto_download_response)


def get_link_contract(instance: DocumentsContractEggsModel, parce_str: str) -> str | None:
    """
    Преобразует данные в строку.
    """
    return str(instance.contract) if parce_str == 'contract' else None


def get_link_deal_docs(instance: DocumentsDealEggsModel, parce_str: str) -> str | None:
    """
    Сверяет строчные данные и возвращает линк.
    """
    match parce_str:
        case 'payment_order_incoming':    
            return str(instance.payment_order_incoming)    
        case 'payment_order_outcoming_logic':
            return str(instance.payment_order_outcoming_logic)
        case 'payment_order_outcoming':    
            return str(instance.payment_order_outcoming)    
        case 'specification_seller':    
            return str(instance.specification_seller)    
        case 'account_to_seller': 
            return str(instance.account_to_seller) 
        case 'specification_buyer': 
            return str(instance.specification_buyer) 
        case 'account_to_buyer':
            return str(instance.account_to_buyer)
        case 'application_contract_logic':
            return str(instance.application_contract_logic)
        case 'account_to_logic':
            return str(instance.account_to_logic)
        case 'UPD_incoming': 
            return str(instance.UPD_incoming) 
        case 'account_invoicing_from_seller': 
            return str(instance.account_invoicing_from_seller) 
        case 'product_invoice_from_seller':
            return str(instance.product_invoice_from_seller)
        case 'UPD_outgoing': 
            return str(instance.UPD_outgoing) 
        case 'account_invoicing_from_buyer':
            return str(instance.account_invoicing_from_buyer)
        case 'product_invoice_from_buyer': 
            return str(instance.product_invoice_from_buyer)
        case 'veterinary_certificate_buyer':
            return str(instance.veterinary_certificate_buyer)
        case 'veterinary_certificate_seller':
            return str(instance.veterinary_certificate_seller)
        case 'international_deal_CMR': 
            return str(instance.international_deal_CMR) 
        case 'international_deal_TTN': 
            return str(instance.international_deal_TTN) 
        case 'UPD_logic':
            return str(instance.UPD_logic)
        case 'account_invoicing_logic':
            return str(instance.account_invoicing_logic)
        case 'product_invoice_logic': 
            return str(instance.product_invoice_logic) 
        case _:
            return None


def get_half_link_for_save(document_name: str) -> str:
    return(f'uploads/deal_docs/{document_name}/{datetime.today().year}/{datetime.today().month}/' + 
        f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/')


