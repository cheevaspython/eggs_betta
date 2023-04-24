from datetime import datetime
from typing import Union

from rest_framework import serializers

from product_eggs.models.documents import DocumentsContractEggsModel, \
    DocumentsDealEggsModel
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs


def update_and_save_data_number_json(
        docs_nums_date_dict: dict,
        instance: DocumentsDealEggsModel | DocumentsContractEggsModel, 
        cash: bool = False) -> None:
    """
    Обновляет и сохраняет данные по значимым платежным документам.
    """
    if cash and isinstance(instance, DocumentsContractEggsModel):
        instance.data_number_json_cash.update(
            {str(datetime.today())[:-7]: docs_nums_date_dict})
        instance.save()
    else:
        instance.data_number_json.update(
            {str(datetime.today())[:-7]: docs_nums_date_dict})
        instance.save()


def try_to_get_documents_model(documents_id: int) -> DocumentsContractEggsModel:
    """
    Получает модель DocumentsContractEggsModel по pk
    """
    try:
        return DocumentsContractEggsModel.objects.get(pk=documents_id)
    except KeyError:
        raise serializers.ValidationError('entry documents_id is not valid')


def create_docs_conteragent_model(
        instance: Union[BuyerCardEggs, SellerCardEggs, LogicCardEggs]) -> None:
    """
    Создает внешний ключ на модель DocumentsContractEggsModel.
    """
    instance.documents_contract = DocumentsContractEggsModel.objects.create()
    instance.save()   

