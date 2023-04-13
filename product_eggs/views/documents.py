from datetime import datetime, date

from rest_framework import permissions

from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from product_eggs.services.documents import parse_multy_payment_json, try_to_write_date_nums_jsonfield, \
    deal_docs_dict_json_update
from product_eggs.services.documents import cash_documents_check_save
from product_eggs.models.custom_model_viewset import CustomModelViewSet
from product_eggs.models.documents import DocumentsDealEggsModel, DocumentsBuyerEggsModel, \
    DocumentsContractEggsModel
from product_eggs.serializers.documents_serializers import DocumentsDealEggsSerializer, \
    DocumentsBuyerSerializer, DocumentsContractEggsSerializer
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser


class DocumentsDealEggsModelViewSet(CustomModelViewSet): 
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentsDealEggsModel.objects.all()
    serializer_class = DocumentsDealEggsSerializer

    def perform_update(self, serializer, instance):
        try:
            if serializer.validated_data['tmp_json']:
                try_to_write_date_nums_jsonfield(
                    serializer.validated_data['tmp_json'],
                    eq_requestuser_is_customuser(self.request.user),
                    instance,
                )
                instance.tmp_json = {}
                instance.save()

        except KeyError:
            pass

        deal_docs_dict_json_update(serializer.validated_data, 
                eq_requestuser_is_customuser(self.request.user), instance)


class DocumentsBuyerCashViewSet(CustomModelViewSet): 
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentsBuyerEggsModel.objects.all()
    serializer_class = DocumentsBuyerSerializer

    def perform_update(self, serializer, instance):
        try:
            if serializer.validated_data['tmp_json']:
                cash_documents_check_save(serializer.validated_data['tmp_json'],  
                    eq_requestuser_is_customuser(self.request.user), instance)
                parse_multy_payment_json(
                    serializer.validated_data['tmp_json'],
                    eq_requestuser_is_customuser(self.request.user),
                    None,
                )
                instance.tmp_json = {}
                instance.save()
        except KeyError:
            pass
        try:
            if serializer.validated_data['buyer_cash_docs']:
                instance.cash_links_dict_json.update(
                    {str(datetime.today())[:-7]: (doc_buyer_cash +
                        str(serializer.validated_data['buyer_cash_docs']))})
                instance.save()
        except KeyError:
            pass


class DocumentsContractViewSet(CustomModelViewSet): 
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentsContractEggsModel.objects.all()
    serializer_class = DocumentsContractEggsSerializer

    def perform_update(self, serializer, instance):
        try:
            if serializer.validated_data['multi_pay_order']:
                instance.multi_pay_order_links_dict_json.update(
                    {str(datetime.today())[:-7] : (doc_contract_multy_pay +
                        str(serializer.validated_data['multi_pay_order']))}
                )
                parse_multy_payment_json(
                    serializer.validated_data['tmp_json_for_multi_pay_order'],
                    eq_requestuser_is_customuser(self.request.user),
                    instance,
                )
        except KeyError:
            pass
        try:
            if serializer.validated_data['contract']:
                instance.contract_links_dict_json.update(
                    {str(datetime.today())[:-7]: (doc_contract_contract +
                        str(serializer.validated_data['contract']))}
                )
        except KeyError:
            pass

        instance.tmp_json_for_multi_pay_order = {}
        instance.save()


def check_serializer_val_data(funk): #@deacorator
    try:
        return funk()
    except KeyError:
        pass


doc_buyer_cash = f'uploads/buyer_cash_docs/{date.today().year}/{date.today().month}/{date.today().day}/'
doc_contract_contract = f'uploads/contragents_docs/contracts/{date.today().year}/{date.today().month}/{date.today().day}/'
doc_contract_multy_pay = f'uploads/contragents_docs/multy_pay_order/{date.today().year}/{date.today().month}/{date.today().day}/'









