from datetime import datetime
from typing import Union

from rest_framework import serializers

from product_eggs.models.documents import DocumentsBuyerEggsModel, DocumentsContractEggsModel, \
    DocumentsDealEggsModel
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs


def update_and_save_data_number_json(
    docs_nums_date_dict: dict,
    instance: DocumentsDealEggsModel | DocumentsContractEggsModel | DocumentsBuyerEggsModel) -> None:
    """
    Обновляет и сохраняет данные по значимым платежным документам.
    """
    instance.data_number_json.update({str(datetime.today())[:-7]: docs_nums_date_dict})
    instance.save()


def try_to_get_documents_model(documents_id: int) -> DocumentsContractEggsModel:
    """
    Получает модель DocumentsContractEggsModel по pk
    """
    try:
        return DocumentsContractEggsModel.objects.get(pk=documents_id)
    except KeyError:
        raise serializers.ValidationError('entry documents_id is not valid')


def create_docs_cash_buyer() -> DocumentsBuyerEggsModel:
    """
    Создает новую модель DocumentsBuyerEggsModel. 
    """
    new_docs_cash = DocumentsBuyerEggsModel.objects.create()
    new_docs_cash.save()
    return new_docs_cash


def create_docs_cash_model(instance: BuyerCardEggs) -> None:
    """
    Создает внешний ключ на модель документов по форме 2.
    """
    if instance.docs_cash is None:
        instance.docs_cash = create_docs_cash_buyer()
        instance.save()   
    else:
        return print('docs_cash not None')


def create_docs_conteragent_model(instance: Union[BuyerCardEggs, SellerCardEggs]) -> None:
    """
    Создает внешний ключ на модель DocumentsContractEggsModel.
    """
    instance.documents_contract = DocumentsContractEggsModel.objects.create()
    instance.save()   

