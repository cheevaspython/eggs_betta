import uuid

from abc import ABC, abstractmethod

from dataclasses import asdict

from datetime import datetime

from typing import Union

from rest_framework import serializers

from product_eggs.models.documents import DocumentsContractEggsModel, DocumentsDealEggsModel
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.services.data_class.data_class_documents import (
    PayOrderDataForSave, PayOrderDataForSaveMultiClear
)
from product_eggs.services.decorators import try_decorator_param


class DataNumberJsonUpdaterInterface(ABC):
    '''
    Интерфейс работы с балансом клиента.
    '''
    @abstractmethod
    @try_decorator_param(('AttributeError',))
    def data_number_json_saver(self):
        """
        Cохраняет данные по значимым платежным документам.
        """


class DataNumberJsonSaver(DataNumberJsonUpdaterInterface):

    def __init__(self,
            docs_nums_date: PayOrderDataForSaveMultiClear | PayOrderDataForSave,
            instance: DocumentsDealEggsModel | DocumentsContractEggsModel,
            cash: bool = False,
            general_uuid: str | None = None) -> None:
        self.docs_nums_date_dict = asdict(docs_nums_date)
        self.instance = instance
        self.cash = cash
        if general_uuid:
            self.general_uuid = general_uuid
        else:
            self.general_uuid = str(datetime.today())[:-7] + ' , ' + str(uuid.uuid4())

    def data_number_json_saver(self):
        if self.cash:
            self.instance.data_number_json_cash.update(
                {self.general_uuid: self.docs_nums_date_dict})
            self.instance.save()
        else:
            self.instance.data_number_json.update(
                {self.general_uuid: self.docs_nums_date_dict})
            self.instance.save()

    def multy_pay_json_saver(self):
        if isinstance(self.instance, DocumentsContractEggsModel):
            self.instance.multy_pay_json.update(
                {self.general_uuid: self.docs_nums_date_dict})
            self.instance.save()


def create_docs_conteragent_model(
        instance: Union[BuyerCardEggs, SellerCardEggs, LogicCardEggs]) -> None:
    """
    Создает внешний ключ на модель DocumentsContractEggsModel.
    """
    instance.documents_contract = DocumentsContractEggsModel.objects.create()
    instance.save()





