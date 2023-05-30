from dataclasses import asdict
from datetime import datetime
from typing import Union

from rest_framework import serializers

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsContractEggsModel, \
    DocumentsDealEggsModel
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.get_anything.try_to_get_models import get_client_for_inn, \
    try_to_get_deal_model_for_doc_deal_id
from product_eggs.services.data_class import OtherPayTmpData, PayOrderDataForSave, \
    PayOrderDataForSaveMulti
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from product_eggs.services.statistic import ContragentBalanceForm
from product_eggs.services.documents.documents_get import update_and_save_data_number_json
from users.models import CustomUser


class DealDocumentsPaymentParser():
    """
    Обрабатывает вводимые данные по значимым платежным документам.
    Создает dataclass и взаимодействует с DealPayOrderUPDservice 
    Записывает данные в случае корректности, либо raise error.
    """
    def __init__(self, 
            payment_data: dict,
            user: CustomUser,
            instance: DocumentsDealEggsModel):

        self.pay_data = payment_data
        self.user = user
        self.instance = instance
        self.deal = try_to_get_deal_model_for_doc_deal_id(instance.pk)

    def check_entry_data(self) -> bool:
        if isinstance(self.deal, BaseDealEggsModel): 
            # status_check(self.deal, (3, 4,)) #TODO
            self.pay_client  = get_client_for_inn(self.pay_data['inn']) 
            if isinstance(self.pay_client, Union[SellerCardEggs, BuyerCardEggs, LogicCardEggs]):
                self.client_documents_model = self.pay_client.documents_contract
                return True
            else:
                raise serializers.ValidationError('client id is not valid')
        else:
            raise serializers.ValidationError('deal id invalid. check entry data')
        
    def update_pay_data(self):
        self.pay_data['user'] = self.user.pk
        self.pay_data['deal'] = self.deal.pk
        self.pay_data['documents_id'] = self.instance.pk

    def convert_pay_data(self):
        self.converted_pay_data = PayOrderDataForSave(**self.pay_data) 

    def update_model_field(self):
        update_and_save_data_number_json(self.pay_data, self.instance)
        if self.client_documents_model:
            update_and_save_data_number_json(
                self.pay_data, self.client_documents_model)

    def deal_service_create_and_action(self):
        from product_eggs.services.base_deal.deal_pay_service import DealPayOrderUPDservice 
        if self.pay_client:
            self.deal_service_object = DealPayOrderUPDservice(
                self.converted_pay_data,
                self.deal,
                self.pay_client,
                ContragentBalanceForm(
                    current_model=self.deal,
                    pay_client=self.pay_client,
                    money_amount=float(self.converted_pay_data.pay_quantity),
                )
            )
            self.deal_service_object.try_to_create_payback_date_if_UPD_update()
            self.deal_service_object.add_or_replay_deal_debt() 

    def main_default(self):
        self.check_entry_data()
        self.update_pay_data()
        self.convert_pay_data()
        self.update_model_field()
        self.deal_service_create_and_action()
        self.deal_service_object.deal.save()

    def save_deal_service(self):
        self.deal_service_object.deal.save()


class MultiDocumentsPaymentParser():
    """
    Обрабатывает вводимые данные по значимым платежным документам.
    Создает dataclass и взаимодействует с DealPayOrderUPDservice 
    Записывает данные в случае корректности, либо raise error.
    при общем платежном поручении.
    """
    def __init__(self,
            multi_pay_data: dict,
            user: CustomUser,
            current_document_contract: DocumentsContractEggsModel | None,
            cur_tail: TailsContragentModelEggs | None = None,
            cash: bool = False):
        self._multi_pay_data = multi_pay_data
        self.user = user
        self.doc_contract = current_document_contract
        self._multi_pay_data['user'] = self.user.pk
        self.save_data_for_update = list()
        self.cash = cash
        self.cur_tail = cur_tail

    @try_decorator_param(('TypeError',))
    def convert_pay_multi_data(self):
        self.pay_order_multi = PayOrderDataForSaveMulti(**self._multi_pay_data) 

    def check_entry_data(self) -> bool:
        if self.convert_pay_multi_data:
            if get_client_for_inn(self.pay_order_multi.inn):
                self.client = get_client_for_inn(self.pay_order_multi.inn)
                return True
        raise serializers.ValidationError('wrong data in tmp_multy_json')

    def get_documents_contract(self):
        if self.client:
            if self.doc_contract == None:
                self.doc_contract = DocumentsContractEggsModel.objects.get(
                    pk=self.client.documents_contract.pk)
        else:
            raise serializers.ValidationError(
                'Error in MultyDocumentsPaymentParser, wrong inn client or doc_contract'
            )

    def construct_other_pay(self, cur_deal_pay: dict) -> dict:
        tmp_asdict = asdict(self.pay_order_multi)
        tmp_asdict.pop('other_pays', None)
        tmp_asdict.pop('total_amount', None)
        tmp_asdict.pop('tail_form_one', None)
        tmp_asdict.pop('tail_form_two', None)
        tmp_asdict.update(asdict(cur_deal_pay))
        return tmp_asdict
        
    def save_and_update_cur_model(self):
        for obj in self.save_data_for_update:
            obj.current_pay.save_deal_service()
            update_and_save_data_number_json(
                obj.construct, obj.current_deal_doc)

    def send_message_to_finance_manager(self):
        if self.client:
            message = MessageLibrarrySend(
                'message_to_finance_director',
                self.client,
                f"ПП от {self.client}/{self.pay_order_multi.inn}" + 
                f"на сумму {self.pay_order_multi.total_amount}",
            )
            message.send_message()

    def splitter_multi_order(self):
        self.check_entry_data()
        if self.pay_order_multi.other_pays:
            for cur_deal_pay in self.pay_order_multi.other_pays:
                construct = self.construct_other_pay(cur_deal_pay)
                deal_docs = DocumentsDealEggsModel.objects.get(pk=cur_deal_pay.documents_id)
                cur_other_pay = DealDocumentsPaymentParser(
                    construct,
                    self.user,
                    deal_docs,
                )
                cur_other_pay.check_entry_data()
                cur_other_pay.convert_pay_data()
                cur_other_pay.deal_service_create_and_action()
                self.save_data_for_update.append(
                    OtherPayTmpData(
                        cur_other_pay,
                        construct,
                        deal_docs
                        )
                )
                self.save_and_update_cur_model()
        
        self.multi_pay_dict = asdict(self.pay_order_multi)
        self.get_documents_contract()
        self.send_message_to_finance_manager()

    def tail_save(self):
        from product_eggs.services.tails import tails_treatment
        if self.cur_tail:
            tails_treatment(self.multi_pay_dict, cur_tail=self.cur_tail)
        elif self.client:
            if isinstance(self.client, LogicCardEggs):
                pass
            else:
                if self.multi_pay_dict['tail_form_one'] or \
                        self.multi_pay_dict['tail_form_two']:
                    self.multi_pay_dict.pop('other_pays', None)
                    tails_treatment(self.multi_pay_dict, client=self.client)
    
    def update_multi_pay_doc_model_json(self):
        if self.doc_contract:
            self.doc_contract.multy_pay_json.update( 
                {str(datetime.today())[:-7]: self.multi_pay_dict})

    def update_data_num_doc_model_json(self):
        if self.doc_contract:
            if self.cash:
                update_and_save_data_number_json(
                    self.multi_pay_dict, 
                    self.doc_contract,
                    cash=True)
            else:
                update_and_save_data_number_json(
                    self.multi_pay_dict, 
                    self.doc_contract)

    def main(self):
        """
        start class process.
        """
        self.convert_pay_multi_data()
        self.check_entry_data()
        self.get_documents_contract()
        self.splitter_multi_order()
        self.tail_save()
        self.update_multi_pay_doc_model_json()
        self.update_data_num_doc_model_json()

