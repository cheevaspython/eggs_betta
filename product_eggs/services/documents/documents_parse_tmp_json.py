import uuid
from datetime import datetime
from collections.abc import Iterable
from dataclasses import asdict
from typing import Union

from product_eggs.models.documents import (
    DocumentsContractEggsModel, DocumentsDealEggsModel
)
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.services.base_deal.deal_services import status_check
from product_eggs.services.data_class.data_class_documents import (
    OtherPays, PrePayOrderDataForSave, PrePayOrderDataForSaveMulti
)
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.get_anything.try_to_get_models import (
    get_client_for_inn, try_to_get_deal_model_for_doc_deal_id
)
from product_eggs.services.data_class import (
    PayOrderDataForSave,
    PayOrderDataForSaveMulti, PayOrderDataForSaveMultiClear
)
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from product_eggs.services.documents.documents_get import DataNumberJsonSaver
from product_eggs.services.validationerror import custom_error
from product_eggs.tasks.deal_status_closer import check_and_close_deal

from users.models import CustomUser


class DealDocumentsPaymentParser():
    """
    Обрабатывает вводимые данные по значимым платежным документам.
    Создает dataclass и взаимодействует с DealPayOrderUPDservice
    Записывает данные в случае корректности, либо raise error.
    """
    def __init__(
            self,
            payment_data: PrePayOrderDataForSave,
            user: CustomUser,
            instance: DocumentsDealEggsModel,
            general_uuid: str | None = None):

        self.pay_data = asdict(payment_data)
        self.cash = payment_data.cash
        self.user = user
        self.instance = instance
        self.deal = try_to_get_deal_model_for_doc_deal_id(instance.pk)
        self.client_documents_model: DocumentsContractEggsModel = self._check_entry_data()
        status_check(self.deal, [2, 3, 4])
        self._verificate_cash_and_deal()
        if general_uuid:
            self.general_uuid = general_uuid
        else:
            self.general_uuid = str(datetime.today())[:-7] + ' , ' + str(uuid.uuid4())

    def _verificate_cash_and_deal(self):
        if self.cash:
            match self.pay_data['client_type']:
                case 'seller':
                    raise custom_error('(seller) We pay to seller only form 1!', 433)
                case 'buyer':
                    if not self.deal.cash:
                        raise custom_error('(buyer) tmp_json -> cash, but deal.cash false!', 433)
                case 'logic':
                    if self.deal.delivery_form_payment != 3:
                        raise custom_error('(logic) tmp_json -> cash, but deal.delivery_form_payment !=3 !', 433)
                case _:
                    raise custom_error('wronf client_type in DealDocumentsPaymentParser', 433)

    def _check_entry_data(self) -> DocumentsContractEggsModel:
        self.pay_client  = get_client_for_inn(self.pay_data['inn'], self.pay_data['client_type'])
        if isinstance(self.pay_client, Union[SellerCardEggs, BuyerCardEggs, LogicCardEggs]) and self.pay_client.documents_contract:
            return self.pay_client.documents_contract
        else:
            raise custom_error('pay client not found', 433)

    def _update_pay_data(self) -> None:
        self.pay_data['user'] = self.user.pk
        self.pay_data['deal'] = self.deal.pk
        self.pay_data['documents_id'] = self.instance.pk
        del self.pay_data['cash']
        try:
            self.pay_data['pay_quantity'] = float(self.pay_data['pay_quantity'])
        except ValueError as e:
            raise custom_error(f'wrong doc type in tmp_json {e}', 433)

    def _convert_pay_data(self) -> None:
        self.converted_pay_data = PayOrderDataForSave(**self.pay_data)

    def _update_model_field(self):
        DataNumberJsonSaver(
            self.converted_pay_data, self.instance, self.cash, general_uuid=self.general_uuid
        ).data_number_json_saver()
        DataNumberJsonSaver(
            self.converted_pay_data, self.client_documents_model, self.cash, general_uuid=self.general_uuid
        ).data_number_json_saver()

    def _deal_service_create_action(self) -> None:
        from product_eggs.services.base_deal.deal_pay_service import DealPayOrderUPDservice
        if self.pay_client:
            self.deal_service_object = DealPayOrderUPDservice(
                self.converted_pay_data,
                self.deal,
                self.pay_client,
            )
            self.deal_service_object.try_to_create_payback_date_if_UPD_update()
            self.deal_service_object.add_or_replay_deal_debt()

    def main_default(self) -> None:
        self._check_entry_data()
        self._update_pay_data()
        self._convert_pay_data()
        self._deal_service_create_action()
        self._update_model_field()
        self.deal_service_object.deal.save()
        check_and_close_deal(self.deal_service_object.deal, self.user, self.converted_pay_data.date)


class MultiDocumentsPaymentParser():
    """
    Обрабатывает вводимые данные по значимым платежным документам.
    Создает dataclass и взаимодействует с DealPayOrderUPDservice
    Записывает данные в случае корректности, либо raise error.
    при общем платежном поручении.
    """
    def __init__(self,
            multi_pay_data: PrePayOrderDataForSaveMulti,
            user: CustomUser,
            current_doc_contract: DocumentsContractEggsModel | None,
            ):

        self._multi_pay_data = asdict(multi_pay_data)
        self.user = user
        self.doc_contract = current_doc_contract
        self._multi_pay_data['user'] = self.user.pk
        self.cash = multi_pay_data.cash
        self.doc_type = multi_pay_data.doc_type
        self.general_uuid = str(datetime.today())[:-7] + ' , ' + str(uuid.uuid4())
        del self._multi_pay_data['cash']
        del self._multi_pay_data['doc_type']

    @try_decorator_param(('TypeError',))
    def _convert_pay_multi_data(self) -> PayOrderDataForSaveMulti | None:
        self.pay_order_multi = PayOrderDataForSaveMulti(**self._multi_pay_data)

    @try_decorator_param(('AttributeError',))
    def _check_entry_data(self) -> bool:
        if self.pay_order_multi:
            if get_client_for_inn(self.pay_order_multi.inn, self.pay_order_multi.client_type):
                self.client = get_client_for_inn(self.pay_order_multi.inn, self.pay_order_multi.client_type)
                return True
        raise custom_error('wrong data in tmp_multy_json', 433)

    @try_decorator_param(('AttributeError',))
    def _get_documents_contract(self) -> None:
        if self.client and self.client.documents_contract:
            if self.doc_contract == None:
                self.doc_contract = DocumentsContractEggsModel.objects.get(
                    pk=self.client.documents_contract.pk)
        else:
            raise custom_error(
                'Error in MultyDocumentsPaymentParser, wrong inn client or doc_contract', 433)

    @try_decorator_param(('ValueError', 'AttributeError', ))
    def _construct_other_pay(self, cur_deal_pay: OtherPays) -> PrePayOrderDataForSave:
        pre_data =  PrePayOrderDataForSave(
            date=self.pay_order_multi.date,
            number=self.pay_order_multi.number,
            pay_quantity=str(cur_deal_pay.pay_quantity),
            inn=self.pay_order_multi.inn,
            cash=self.cash,
            entity=self.pay_order_multi.entity,
            doc_type=self.doc_type,
            client_type=self.pay_order_multi.client_type,
        )
        return pre_data

    @try_decorator_param(('AttributeError', ))
    def _get_deal_docs_model(self, docs_id: str) -> DocumentsDealEggsModel:
        return DocumentsDealEggsModel.objects.get(pk=int(docs_id))

    def _send_message_to_finance_manager(self):
        if self.client:
            message = MessageLibrarrySend(
                'message_to_finance_director',
                self.client,
                f"ПП от {self.client}/{self.pay_order_multi.inn}" +
                f"на сумму {self.pay_order_multi.total_amount}",
            )
            message.send_message()

    def _splitter_multi_order(self) -> None:
        if self.pay_order_multi.other_pays and isinstance(self.pay_order_multi.other_pays, Iterable):
            for cur_deal_pay in self.pay_order_multi.other_pays:
                cur_other_pay = DealDocumentsPaymentParser(
                    self._construct_other_pay(cur_deal_pay),
                    self.user,
                    self._get_deal_docs_model(cur_deal_pay.deal_docs_pk),
                    self.general_uuid,
                )
                cur_other_pay.main_default()
        self._send_message_to_finance_manager()

    def _tail_save(self) -> None:
        from product_eggs.services.tails.tails import TailsTreatment
        if self.client:
            TailsTreatment(
                self.pay_order_multi,
                self.client,
                self.general_uuid
            ).add_dict_json()

    def _update_data_num_doc_model_json(self) -> None:
        if self.doc_contract and isinstance(self.doc_contract, DocumentsContractEggsModel):
            save_data = PayOrderDataForSaveMultiClear(
                user=self.user.pk,
                date=self.pay_order_multi.date,
                number=self.pay_order_multi.number,
                inn=self.pay_order_multi.inn,
                entity=self.pay_order_multi.entity,
                total_amount=float(self.pay_order_multi.total_amount),
            )
            saver_obj = DataNumberJsonSaver(
                save_data,
                self.doc_contract,
                general_uuid=self.general_uuid
            )
            saver_obj.multy_pay_json_saver()
        else:
            raise custom_error(
                'Multi pay data wrong, cant get doc_contract instance or get wrong model', 433
            )

    def main(self):
        """
        start class process.
        """
        self._convert_pay_multi_data()
        self._check_entry_data()
        self._get_documents_contract()
        self._update_data_num_doc_model_json()
        self._splitter_multi_order()
        self._tail_save()

